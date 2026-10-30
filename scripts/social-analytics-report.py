#!/usr/bin/env python3
"""Learn from LinkedIn and GA4 numbers which wro.cpp posts earn attention.

Subcommands:
  join      Place every LinkedIn row on a blog post (by text), classify the rest, report coverage.
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
import difflib
import importlib.util
import re
import subprocess
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
REPO = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
from schedule_doubles import INTENTIONAL_DOUBLES  # noqa: E402

DEFAULT_WINDOW = "2026-07-30:2026-10-29"
DEFAULT_KIND = "flagship"
NORMAL_HOUR = 8            # the daily auto-scheduler pushes at 08:00Z
END_OF_DAY = "T23:59:59Z"
EXIT_UNRESOLVED = 2
EXIT_NOT_IGNORED = 3
SLOT_COLLISION = "collision"
MIN_LEAD_CHARS = 20        # a caption lead shorter than this is too generic to match a post by prefix
FUZZY_COMPARE_CHARS = 120  # characters of each text compared by similarity when no prefix matches
ORGANIC = "Organic"
CAPTION_HEAD_CHARS = 200   # how much of the caption start is kept as a key for matching LinkedIn text

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
    "slot", "planned_hour", "day_posts", "gap_days", "disturbance", "card_h1", "lead", "caption_head", "caption_words",
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
        "caption_head": " ".join(body.split())[:CAPTION_HEAD_CHARS],
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


class ExportError(Exception):
    """The LinkedIn export is not in the shape this script was written for."""


LINKEDIN_COLUMNS = {
    "text": "Post title", "link": "Post link", "created": "Created date", "impressions": "Impressions",
    "clicks": "Clicks", "reactions": "Likes", "comments": "Comments", "reposts": "Reposts",
}
LINKEDIN_NUMBERS = ("impressions", "clicks", "reactions", "comments", "reposts")
LINKEDIN_DATE_FORMAT = "%m/%d/%Y"


def normalise_text(text: str) -> str:
    """Lowercase ASCII letters and digits only, so spacing, punctuation, accents and quotes never matter."""
    decomposed = unicodedata.normalize("NFKD", text)
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in decomposed if not unicodedata.combining(c)).lower())


def _linkedin_row(raw: dict) -> dict:
    row = {name: raw[column] for name, column in LINKEDIN_COLUMNS.items()}
    row["created"] = datetime.strptime(raw[LINKEDIN_COLUMNS["created"]], LINKEDIN_DATE_FORMAT).date().isoformat()
    for name in LINKEDIN_NUMBERS:
        row[name] = int(float(raw[LINKEDIN_COLUMNS[name]] or 0))
    return row


def read_linkedin_posts(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in LINKEDIN_COLUMNS.values() if c not in (reader.fieldnames or [])]
        if missing:
            raise ExportError(f"{path.name}: missing column(s) {missing}; found {reader.fieldnames}")
        rows = []
        for raw in reader:
            if raw.get("Post type", ORGANIC) != ORGANIC or raw.get("Campaign name", ""):
                raise ExportError(f"{path.name}: a sponsored row ({raw[LINKEDIN_COLUMNS['link']]}); this review is organic-only")
            rows.append(_linkedin_row(raw))
    return rows


@dataclass
class JoinResult:
    rows: list = field(default_factory=list)
    unresolved: list = field(default_factory=list)
    unadvertised: list = field(default_factory=list)
    coverage: float = 1.0


def _days_apart(a: str, b: str) -> int:
    return abs((date.fromisoformat(a) - date.fromisoformat(b)).days)


def _match_key(post: dict) -> str:
    """The start of the caption as sent; the first sentence alone can be too short to tell posts apart."""
    return normalise_text(post.get("caption_head") or post["lead"])


def _by_prefix(text: str, near: list[dict]) -> list[dict]:
    hits = []
    for post in near:
        key = _match_key(post)
        if len(key) >= MIN_LEAD_CHARS and text.startswith(key[:PREFIX_CHARS]):
            hits.append(post)
    return hits


def _by_similarity(text: str, near: list[dict]) -> list[dict]:
    hits = []
    for post in near:
        key = _match_key(post)
        ratio = difflib.SequenceMatcher(None, text[:FUZZY_COMPARE_CHARS], key[:FUZZY_COMPARE_CHARS]).ratio()
        if len(key) >= MIN_LEAD_CHARS and ratio >= FUZZY_MIN:
            hits.append(post)
    return hits


def match_row(row: dict, feats: list[dict], overrides: dict) -> tuple[str, str]:
    """(slug, method). An empty slug with method non-blog or ignore is a decision; with no method, unresolved."""
    decision = overrides.get(row["link"], "")
    if decision.startswith(("non-blog:", "ignore:")):
        return "", decision.split(":", 1)[0]
    if decision:
        return decision, "override"
    near = [f for f in feats if _days_apart(f["date"], row["created"]) <= SLACK_DAYS]
    text = normalise_text(row["text"])
    for method, finder in (("prefix", _by_prefix), ("fuzzy", _by_similarity)):
        hits = finder(text, near)
        same_day = [h for h in hits if h["date"] == row["created"]]
        if len(hits) == 1 or len(same_day) == 1:
            return (same_day or hits)[0]["slug"], method
    return "", ""


def _coverage(rows: list[dict]) -> float:
    counted = [r for r in rows if r["method"] not in ("non-blog", "ignore")]
    total = sum(r["impressions"] for r in counted)
    return sum(r["impressions"] for r in counted if r["slug"]) / total if total else 1.0


def join_posts(li_rows: list[dict], feats: list[dict], overrides: dict) -> JoinResult:
    out = JoinResult()
    for raw in li_rows:
        slug, method = match_row(raw, feats, overrides)
        planned = next((f["date"] for f in feats if f["slug"] == slug), "") if slug else ""
        redated = "1" if planned and planned != raw["created"] else "0"
        out.rows.append({**raw, "slug": slug, "method": method, "multi_send": "0", "redated": redated})
    seen: dict = {}
    for row in out.rows:
        if row["slug"]:
            seen.setdefault(row["slug"], []).append(row)
    for rows in seen.values():
        if len(rows) > 1:
            for row in rows:
                row["multi_send"] = "1"
    out.unresolved = [r for r in out.rows if not r["slug"] and not r["method"]]
    out.unadvertised = sorted(f["slug"] for f in feats if f["slug"] not in seen)
    out.coverage = _coverage(out.rows)
    return out


def _read_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def _read_overrides(path: Path) -> dict:
    return {r["link"]: r["decision"] for r in _read_csv(path)} if path.exists() else {}


def _write_dicts(path: Path, rows: list[dict], columns) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


JOINED_COLUMNS = ("link", "created", "slug", "method", "multi_send", "redated", "impressions", "clicks", "reactions",
                  "comments", "reposts")


def _window_of(li_rows: list[dict], feats: list[dict]) -> list[dict]:
    first, last = min(r["created"] for r in li_rows), max(r["created"] for r in li_rows)
    return [f for f in feats if first <= f["date"] <= last]


def _report_join(out: JoinResult, feats_count: int) -> list[str]:
    matched = sum(bool(r["slug"]) for r in out.rows)
    classified = sum(r["method"] in ("non-blog", "ignore") for r in out.rows)
    lines = [f"matched {matched}/{len(out.rows)} LinkedIn rows ({out.coverage:.1%} of impressions); "
             f"classified non-blog/ignored {classified}; unresolved {len(out.unresolved)}; "
             f"blog posts in range with no LinkedIn row {len(out.unadvertised)} of {feats_count}"]
    lines += [f"  unresolved: {r['link']}  {r['created']}  {r['text'][:70]!r}" for r in out.unresolved]
    return lines


def cmd_join(args: argparse.Namespace) -> int:
    folder = Path(args.dir)
    if not is_safe_to_write(folder / "joined.csv"):
        print(f"refusing to write in {folder}: git does not ignore it, and the repository is public", file=sys.stderr)
        return EXIT_NOT_IGNORED
    try:
        li_rows = read_linkedin_posts(folder / "linkedin-posts.csv")
    except ExportError as error:
        print(f"export problem: {error}", file=sys.stderr)
        return EXIT_UNRESOLVED
    feats = _window_of(li_rows, _read_csv(folder / "features.csv")) if li_rows else []
    out = join_posts(li_rows, feats, _read_overrides(folder / "overrides.csv"))
    _write_dicts(folder / "joined.csv", out.rows, JOINED_COLUMNS)
    _write_dicts(folder / "unadvertised.csv", [{"slug": s} for s in out.unadvertised], ("slug",))
    incomplete = bool(out.unresolved) or out.coverage < COVERAGE_MIN
    print("\n".join(_report_join(out, len(feats))))
    if incomplete:
        print("INCOMPLETE: every row must be placed or classified in overrides.csv" if args.allow_unmatched
              else f"stopping: unresolved rows or coverage below {COVERAGE_MIN:.0%}; use --allow-unmatched to continue")
    return 0 if args.allow_unmatched or not incomplete else EXIT_UNRESOLVED


# ---------------------------------------------------------------------------------------------------------------
# Statistics and the registered verdict rule (docs/analytics.md, "The verdict rule").
# ---------------------------------------------------------------------------------------------------------------

def median(values):
    ordered = sorted(values)
    if not ordered:
        return None
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def quartiles(values):
    ordered = sorted(values)
    half = len(ordered) // 2
    return median(ordered[:half]), median(ordered[len(ordered) - half:])


def median_of(key):
    def stat(rows):
        return median([r[key] for r in rows if r.get(key) is not None])
    return stat


def comment_repost_rate(rows):
    """Comments plus reposts per 1,000 impressions, pooled over the rows, because most posts have none."""
    impressions = sum(r["impressions"] for r in rows)
    return 1000 * sum(r["comments"] + r["reposts"] for r in rows) / impressions if impressions else None


def stat_for(metric):
    return {"imp_index": median_of("imp_index"), "comment_repost_rate": comment_repost_rate,
            "site_sessions_per_1000": median_of("site_per_1000")}[metric]


HYPOTHESES = {
    "H1": {"claim": "a headline with a checkable number or a reframed habit earns more attention",
           "in_a": lambda r: r["hook_number"] == "yes" or r["hook_reframe"] == "yes", "metric": "imp_index"},
    "H2": {"claim": "news earns more attention than evergreen", "in_a": lambda r: r["news"] == "1",
           "metric": "imp_index"},
    "H3": {"claim": "naming a person draws more conversation",
           "in_a": lambda r: r["person_role"] in ("answer", "credit"), "metric": "comment_repost_rate"},
    "H4": {"claim": "a runnable demo brings more readers to the site",
           "in_a": lambda r: r["content_type"] == "demo", "metric": "site_sessions_per_1000"},
}


def imp_index(post, pool):
    """Impressions over the median of the other posts within TREND_DAYS of it, which removes follower growth."""
    others = [p["impressions"] for p in pool if p is not post and _days_apart(p["sent"], post["sent"]) <= TREND_DAYS]
    baseline = median(others)
    return post["impressions"] / baseline if baseline else None


def without_best(rows, stat):
    best = max(rows, key=lambda r: (stat([r]) if stat([r]) is not None else float("-inf")))
    return [r for r in rows if r is not best]


def _ratio(stat, a, b):
    top, bottom = (stat(a) if a else None), (stat(b) if b else None)
    return top / bottom if top is not None and bottom else None


def _halves(rows):
    return ([r for r in rows if r["sent"] < SPLIT_DATE], [r for r in rows if r["sent"] >= SPLIT_DATE])


def _halves_usable(a, b):
    smaller = a if len(a) <= len(b) else b
    early, late = _halves(smaller)
    return len(early) >= MIN_PER_HALF and len(late) >= MIN_PER_HALF


def noise_floor(stat, pool):
    """How big a ratio even/odd calendar days alone produce: the size a real effect has to beat."""
    even = [r for r in pool if date.fromisoformat(r["sent"]).toordinal() % 2 == 0]
    odd = [r for r in pool if date.fromisoformat(r["sent"]).toordinal() % 2 == 1]
    placebo = _ratio(stat, even, odd)
    return max(placebo, 1 / placebo) if placebo else 1.0


def _is_supported(out):
    return (out["ratio"] >= EFFECT_RATIO and out["ratio_without_best"] is not None and out["ratio_without_best"] > 1
            and out["ratio_early"] is not None and out["ratio_early"] > 1
            and out["ratio_late"] is not None and out["ratio_late"] > 1 and out["ratio"] > out["noise_floor"])


def _is_contradicted(out):
    return (out["ratio"] <= 1 and out["ratio_early"] is not None and out["ratio_early"] <= 1
            and out["ratio_late"] is not None and out["ratio_late"] <= 1)


def judge(a, b, stat, pool):
    """The registered rule. `pool` is every compared post, for the placebo. Returns the verdict and its numbers."""
    out = {"n_a": len(a), "n_b": len(b), "stat_a": stat(a) if a else None, "stat_b": stat(b) if b else None,
           "ratio": _ratio(stat, a, b), "verdict": "too little data", "lean": "", "ratio_without_best": None,
           "ratio_early": None, "ratio_late": None, "noise_floor": noise_floor(stat, pool), "halves_ok": False}
    if min(len(a), len(b)) < MIN_GROUP or out["ratio"] is None:
        return out
    out["ratio_without_best"] = _ratio(stat, without_best(a, stat), b)
    (a_early, a_late), (b_early, b_late) = _halves(a), _halves(b)
    out["ratio_early"], out["ratio_late"] = _ratio(stat, a_early, b_early), _ratio(stat, a_late, b_late)
    out["halves_ok"] = _halves_usable(a, b)
    out["lean"] = "A" if out["ratio"] > 1 else "B"
    if out["halves_ok"] and _is_supported(out):
        out["verdict"] = "supported"
    elif out["halves_ok"] and _is_contradicted(out):
        out["verdict"] = "contradicted"
    return out


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
    join = sub.add_parser("join", help="place each LinkedIn row on a blog post and report coverage")
    join.add_argument("--dir", required=True, help="folder holding features.csv and linkedin-posts.csv")
    join.add_argument("--allow-unmatched", action="store_true", help="write the files anyway, marked INCOMPLETE")
    args = parser.parse_args(argv)
    return cmd_join(args) if args.command == "join" else cmd_features(args)


if __name__ == "__main__":
    sys.exit(main())
