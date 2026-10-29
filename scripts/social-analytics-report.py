#!/usr/bin/env python3
"""Learn from LinkedIn and GA4 numbers which wro.cpp posts earn attention.

Subcommands:
  features  Build one row per blog post in a date window from the repository alone (no analytics data
            needed): kind, topic, news, content type, slot, gap, the card headline and caption lead as they
            were when the post went out, and a candidate flag for a number in the hook. It also writes a
            label template for the columns that need a human or a blind labeller.

Raw exports and per-post tables are private. The repository is public, so every output directory must be
ignored by git, and the script refuses to write anywhere else (exit 3).

Usage:
  scripts/social-analytics-report.py features --window 2026-07-30:2026-10-29 --out .notes/analytics/2026-10
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
from schedule_doubles import INTENTIONAL_DOUBLES  # noqa: E402

DEFAULT_WINDOW = "2026-07-30:2026-10-29"
DEFAULT_KIND = "flagship"
NORMAL_HOUR = 8            # the daily auto-scheduler pushes at 08:00Z
END_OF_DAY = "T23:59:59Z"
EXIT_NOT_IGNORED = 3
SLOT_COLLISION = "collision"

# Pre-registered before any export was opened. docs/analytics.md holds the same values in a block that a
# test compares with these names, so neither can change without the other and without a visible diff.
MATURITY_DAYS = 7          # posts younger than this at export time are listed, not compared
MIN_GROUP = 10             # a group smaller than this never gives a verdict
EFFECT_RATIO = 1.5         # the median ratio a hypothesis must reach to count as supported
OUTLIER_MULTIPLE = 5       # a post above this many times the median impressions is an outlier
TREND_DAYS = 7             # imp_index compares a post with its neighbours within this many days
FIRST_DAYS = 3             # the days after sending that count as "first" for site sessions
SPLIT_DATE = "2026-09-13"  # a supported verdict must also hold on both sides of this date
MIN_PER_HALF = 5           # the smaller group needs this many posts on each side of the split
AGREEMENT_MIN = 0.8        # labels below this agreement between two passes are tightened and redone
COVERAGE_MIN = 0.95        # the report is complete only if this share of impressions is matched
PREFIX_CHARS = 60          # the text prefix compared when a LinkedIn row has no wro.cpp link
SLACK_DAYS = 3             # how far a matched caption may sit from the LinkedIn post date
FUZZY_MIN = 0.85           # the minimum similarity for a fuzzy text match, unique matches only
PRIMARY_METRICS = {
    "H1": "imp_index",
    "H2": "imp_index",
    "H3": "comment_repost_rate",
    "H4": "site_sessions_per_1000",
}

# Days that went wrong for reasons outside the content, so their posts are never compared.
DISTURBANCES = {
    "2026-08-27": "deploy-cron-delay",
    "2026-08-28": "deploy-cron-delay",
    "2026-09-01": "redate-collision",
    "2026-09-02": "redate-collision",
}

# First match wins, so a post tagged both reflection and qt counts as qt.
TAG_GROUPS = (
    ("qt", {"qt", "moc", "models", "signals"}),
    ("reflection", {"reflection"}),
    ("safety", {"safety", "security", "contracts", "verification", "sanitizers", "correctness", "lifetime"}),
    ("performance", {"performance", "memory", "pmr", "allocators", "concurrency", "threads"}),
    ("committee", {"wg21", "cpp29", "standardization", "proposal", "mailing", "conferences", "cppcon", "community"}),
    ("tooling", {"gcc", "clang", "tooling", "testing", "toolchain", "libcxx", "llvm", "conformance", "portability"}),
    ("stdlib", {"stdlib", "ranges", "containers", "json", "enums", "functional", "logging",
                "structured-bindings", "modules"}),
    ("libraries", {"regex", "ctre", "mp-units", "units"}),
)
OTHER_GROUP = "other"

FEATURE_COLUMNS = (
    "slug", "date", "kind", "title", "summary", "series", "series_order", "tags", "news", "content_type", "topic_group",
    "slot", "planned_hour", "day_posts", "gap_days", "disturbance", "card_h1", "lead", "caption_words",
    "h1_number_candidate", "lead_number_candidate",
)
LABEL_COLUMNS = ("slug", "hook_reframe", "hook_number", "person_role", "note")

_MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December|"
           "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec")
_UNITS = r"ms|us|ns|s|x|%|MB|KB|GB|B"
# Removed before looking for a quantity: versions, standards, papers, years, dates, times, prices, tickets.
_NOT_A_QUANTITY = [re.compile(p, re.IGNORECASE) for p in (
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"C\+\+\s?\d{2}\b",
    r"\b[PN]\d{4}(R\d+)?\b",
    r"\b[A-Z]{2,4}\d{3,5}\b",
    r"\b(GCC|Clang|LLVM|MSVC|Qt|FFmpeg|Boost|Python|Rust|Swift|CMake)\s+v?\d+(\.\d+)*",
    rf"(?<![\w.])v?\d+(\.\d+)+(?!\w)(?!\s*({_UNITS})\b)",
    r"\b20\d{2}\b",
    rf"\b\d{{1,2}}\s+({_MONTHS})\b",
    rf"\b({_MONTHS})\s+\d{{1,2}}\b",
    r"\b\d{1,2}:\d{2}Z?\b",
    r"[$€£]\s?\d[\d.,]*",
    r"\b\d+\s?(USD|EUR|PLN)\b",
    r"[#!]\d+\b",
)]
_QUANTITY = re.compile(
    r"\d|\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|dozen|hundred|thousand|million|"
    r"twice|double|triple|half)\b", re.IGNORECASE)
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")
_URL = re.compile(r"https?://\S+")


@dataclass(frozen=True)
class Post:
    slug: str
    date: str
    kind: str
    title: str
    summary: str
    tags: tuple[str, ...]
    series: str
    series_order: str
    body: str


def parse_frontmatter(text: str) -> dict:
    """Flat `key: value` lines and `[a, b]` lists, which is all the posts use."""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    out: dict = {}
    for line in parts[1].splitlines():
        key, sep, value = line.partition(":")
        if sep and key.strip() and not key.startswith((" ", "\t")):
            out[key.strip()] = _frontmatter_value(value.strip())
    return out


def _frontmatter_value(raw: str):
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip().strip("'\"") for item in raw[1:-1].split(",") if item.strip()]
    return raw.strip("'\"") if raw[:1] in "'\"" else raw


def hook_number(text: str) -> bool:
    """Candidate only: does the text hold a quantity claim once versions, years and dates are removed?"""
    for pattern in _NOT_A_QUANTITY:
        text = pattern.sub(" ", text)
    return bool(_QUANTITY.search(text))


def topic_group(tags) -> str:
    for group, members in TAG_GROUPS:
        if members & set(tags):
            return group
    return OTHER_GROUP


def content_type(body: str) -> str:
    if "<GodboltEmbed" in body:
        return "demo"
    return "code" if "```" in body else "commentary"


def load_posts(root: Path) -> list[Post]:
    posts = []
    for path in sorted((root / "src" / "content" / "posts").glob("*.mdx")):
        text = path.read_text()
        fm = parse_frontmatter(text)
        posts.append(Post(
            slug=fm.get("slug", path.stem), date=fm["pubDate"], kind=fm.get("kind", DEFAULT_KIND),
            title=fm.get("title", ""), summary=fm.get("summary", ""),
            tags=tuple(fm.get("tags", [])), series=fm.get("series", ""),
            series_order=fm.get("series_order", ""), body=text.split("---", 2)[2]))
    return posts


def slot_and_hour(post: Post, doubles: dict, collisions: set) -> tuple[str, int]:
    if post.date in collisions:
        return SLOT_COLLISION, NORMAL_HOUR
    planned = doubles.get(post.date)
    if planned and planned["slug"] == post.slug:
        return "2", int(planned["hour"])
    return "1", NORMAL_HOUR


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def file_as_sent(root: Path, relpath: str, day: str) -> str:
    """The file as it was committed on or before `day`, else its first version, else the working copy."""
    path = root / relpath
    if not path.exists():
        return ""
    commit = _git(root, "log", "-1", f"--before={day}{END_OF_DAY}", "--format=%H", "--", relpath)
    if not commit:
        commit = _git(root, "log", "--diff-filter=A", "--reverse", "--format=%H", "--", relpath).split("\n")[0]
    shown = _git(root, "show", f"{commit}:{relpath}") if commit else ""
    return shown or path.read_text()


def card_h1(content_md: str) -> str:
    match = re.search(r"^# (.+)$", content_md, re.MULTILINE)
    return match.group(1).strip() if match else ""


def caption_body(caption_md: str) -> str:
    match = re.search(r"^## Body\s*\n(.*?)(?=^## |\Z)", caption_md, re.MULTILINE | re.DOTALL)
    return _URL.sub("", match.group(1)).strip() if match else ""


def lead_sentence(body: str) -> str:
    return _SENTENCE_END.split(body, maxsplit=1)[0].strip() if body else ""


def _card_columns(root: Path, post: Post) -> dict:
    folder = f"social/linkedin/{post.slug}"
    h1 = card_h1(file_as_sent(root, f"{folder}/content.md", post.date))
    body = caption_body(file_as_sent(root, f"{folder}/caption.md", post.date))
    lead = lead_sentence(body)
    return {
        "card_h1": h1,
        "lead": lead,
        "caption_words": str(len(body.split())) if body else "",
        # Separate columns: the card headline is the hook the style guide means; the lead is a second place.
        "h1_number_candidate": "1" if hook_number(h1) else "0",
        "lead_number_candidate": "1" if hook_number(lead) else "0",
    }


def _gap_days(ordered: list[Post], index: int) -> int:
    if index == 0:
        return 0
    return (date.fromisoformat(ordered[index].date) - date.fromisoformat(ordered[index - 1].date)).days


def build_features(root: Path, start: str, end: str, *, doubles: dict, collisions: set,
                   disturbances: dict) -> list[dict]:
    posts = load_posts(root)
    per_day = {}
    for post in posts:
        per_day[post.date] = per_day.get(post.date, 0) + 1
    ordered = sorted(posts, key=lambda p: (p.date, slot_and_hour(p, doubles, collisions)[0], p.slug))
    rows = []
    for index, post in enumerate(ordered):
        if not start <= post.date <= end:
            continue
        slot, hour = slot_and_hour(post, doubles, collisions)
        rows.append({
            "slug": post.slug, "date": post.date, "kind": post.kind, "title": post.title,
            "summary": post.summary,
            "series": post.series, "series_order": post.series_order, "tags": ";".join(post.tags),
            "news": "1" if "news" in post.tags else "0", "content_type": content_type(post.body),
            "topic_group": topic_group(post.tags), "slot": slot, "planned_hour": str(hour),
            "day_posts": str(per_day[post.date]), "gap_days": str(_gap_days(ordered, index)),
            "disturbance": disturbances.get(post.date, ""), **_card_columns(root, post),
        })
    return rows


def summarise(rows: list[dict]) -> dict:
    days = {}
    for row in rows:
        days[row["date"]] = int(row["day_posts"])
    return {
        "posts": len(rows),
        "flagship": sum(r["kind"] == "flagship" for r in rows),
        "short": sum(r["kind"] == "short" for r in rows),
        "double_days": sum(count >= 2 for count in days.values()),
        "disturbed": sum(bool(r["disturbance"]) for r in rows),
    }


def known_past_collisions() -> set:
    spec = importlib.util.spec_from_file_location("check_pubdates", SCRIPTS / "check-pubdates.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return set(module.KNOWN_PAST_COLLISIONS)


def is_safe_to_write(target: Path) -> bool:
    """A target inside any git work tree must be ignored by that work tree; elsewhere nothing can commit it.

    The work tree is found from the target itself, not from --root, because the data may live in a
    different checkout of the same public repository.
    """
    probe = target.resolve().parent
    while not probe.exists():
        probe = probe.parent
    inside = subprocess.run(["git", "-C", str(probe), "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return True
    return subprocess.run(["git", "-C", str(probe), "check-ignore", "-q", str(target.resolve())]).returncode == 0


def _write_features(out: Path, rows: list[dict]) -> None:
    with open(out / "features.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FEATURE_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def _write_label_template(out: Path, rows: list[dict]) -> int:
    """Append unlabelled rows for new slugs. Existing rows, labelled or not, are never touched."""
    path = out / "labels.csv"
    known = set()
    if path.exists():
        with open(path, newline="") as handle:
            known = {row["slug"] for row in csv.DictReader(handle)}
    new = [r["slug"] for r in rows if r["slug"] not in known]
    with open(path, "a", newline="") as handle:
        writer = csv.writer(handle)
        if not known and not path.stat().st_size:
            writer.writerow(LABEL_COLUMNS)
        writer.writerows([slug] + [""] * (len(LABEL_COLUMNS) - 1) for slug in new)
    return len(new)


def cmd_features(args: argparse.Namespace) -> int:
    root, out = Path(args.root), Path(args.out)
    if not is_safe_to_write(out / "features.csv"):
        print(f"refusing to write {out}: git does not ignore it, and the repository is public", file=sys.stderr)
        return EXIT_NOT_IGNORED
    start, _, end = args.window.partition(":")
    rows = build_features(root, start, end, doubles=INTENTIONAL_DOUBLES, collisions=known_past_collisions(),
                          disturbances=DISTURBANCES)
    out.mkdir(parents=True, exist_ok=True)
    _write_features(out, rows)
    added = _write_label_template(out, rows)
    counts = summarise(rows)
    print(" ".join(f"{key}={value}" for key, value in counts.items()), f"new_label_rows={added}", f"out={out}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    features = sub.add_parser("features", help="one row per post, from the repository alone")
    features.add_argument("--root", default=str(REPO))
    features.add_argument("--window", default=DEFAULT_WINDOW, help="START:END, inclusive, by pubDate")
    features.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    return cmd_features(args)


if __name__ == "__main__":
    sys.exit(main())
