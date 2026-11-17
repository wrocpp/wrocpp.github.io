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
import hashlib
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
CADENCE_FROM = "2026-09-21"  # the first planned double day; the cadence views start here (descriptive, no verdict)
TOP_N = 10                  # posts listed in the private top and bottom tables
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


def _override_result(decision):
    if decision.startswith(("non-blog:", "ignore:")):
        return "", decision.split(":", 1)[0]
    return (decision, "override") if decision else None


def _prefer_same_day(hits, created):
    same_day = [h for h in hits if h["date"] == created]
    return same_day if len(same_day) == 1 else hits


def _text_match(row, feats):
    near = [f for f in feats if _days_apart(f["date"], row["created"]) <= SLACK_DAYS]
    text = normalise_text(row["text"])
    for method, finder in (("prefix", _by_prefix), ("fuzzy", _by_similarity)):
        hits = _prefer_same_day(finder(text, near), row["created"])
        if len(hits) == 1:
            return hits[0]["slug"], method
    return "", ""


def match_row(row: dict, feats: list[dict], overrides: dict) -> tuple[str, str]:
    """(slug, method). An empty slug with method non-blog or ignore is a decision; with no method, unresolved."""
    return _override_result(overrides.get(row["link"], "")) or _text_match(row, feats)


def _coverage(rows: list[dict]) -> float:
    counted = [r for r in rows if r["method"] not in ("non-blog", "ignore")]
    total = sum(r["impressions"] for r in counted)
    return sum(r["impressions"] for r in counted if r["slug"]) / total if total else 1.0


def _redated(slug, created, feats):
    planned = next((f["date"] for f in feats if f["slug"] == slug), "") if slug else ""
    return "1" if planned and planned != created else "0"


def _join_row(raw, feats, overrides):
    slug, method = match_row(raw, feats, overrides)
    return {**raw, "slug": slug, "method": method, "multi_send": "0", "redated": _redated(slug, raw["created"], feats)}


def _flag_multi_send(rows):
    seen: dict = {}
    for row in rows:
        if row["slug"]:
            seen.setdefault(row["slug"], []).append(row)
    for group in seen.values():
        if len(group) > 1:
            for row in group:
                row["multi_send"] = "1"
    return seen


def join_posts(li_rows: list[dict], feats: list[dict], overrides: dict) -> JoinResult:
    out = JoinResult(rows=[_join_row(raw, feats, overrides) for raw in li_rows])
    seen = _flag_multi_send(out.rows)
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


def _join_inputs(folder: Path):
    li_rows = read_linkedin_posts(folder / "linkedin-posts.csv")
    feats = _window_of(li_rows, _read_csv(folder / "features.csv")) if li_rows else []
    return li_rows, feats, _read_overrides(folder / "overrides.csv")


def _join_exit(out: JoinResult, allow: bool) -> int:
    incomplete = bool(out.unresolved) or out.coverage < COVERAGE_MIN
    if incomplete:
        print("INCOMPLETE: every row must be placed or classified in overrides.csv" if allow
              else f"stopping: unresolved rows or coverage below {COVERAGE_MIN:.0%}; use --allow-unmatched to continue")
    return 0 if allow or not incomplete else EXIT_UNRESOLVED


def cmd_join(args: argparse.Namespace) -> int:
    folder = Path(args.dir)
    if not is_safe_to_write(folder / "joined.csv"):
        print(f"refusing to write in {folder}: git does not ignore it, and the repository is public", file=sys.stderr)
        return EXIT_NOT_IGNORED
    try:
        li_rows, feats, overrides = _join_inputs(folder)
    except ExportError as error:
        print(f"export problem: {error}", file=sys.stderr)
        return EXIT_UNRESOLVED
    out = join_posts(li_rows, feats, overrides)
    _write_dicts(folder / "joined.csv", out.rows, JOINED_COLUMNS)
    _write_dicts(folder / "unadvertised.csv", [{"slug": s} for s in out.unadvertised], ("slug",))
    print("\n".join(_report_join(out, len(feats))))
    return _join_exit(out, args.allow_unmatched)


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


def _attach_halves(out, a, b, stat):
    out["ratio_without_best"] = _ratio(stat, without_best(a, stat), b)
    (a_early, a_late), (b_early, b_late) = _halves(a), _halves(b)
    out["ratio_early"], out["ratio_late"] = _ratio(stat, a_early, b_early), _ratio(stat, a_late, b_late)
    out["halves_ok"] = _halves_usable(a, b)
    out["lean"] = "A" if out["ratio"] > 1 else "B"


def _decide(out):
    if out["halves_ok"] and _is_supported(out):
        return "supported"
    return "contradicted" if out["halves_ok"] and _is_contradicted(out) else "too little data"


def judge(a, b, stat, pool):
    """The registered rule. `pool` is every compared post, for the placebo. Returns the verdict and its numbers."""
    out = {"n_a": len(a), "n_b": len(b), "stat_a": stat(a) if a else None, "stat_b": stat(b) if b else None,
           "ratio": _ratio(stat, a, b), "verdict": "too little data", "lean": "", "ratio_without_best": None,
           "ratio_early": None, "ratio_late": None, "noise_floor": noise_floor(stat, pool), "halves_ok": False}
    if min(len(a), len(b)) < MIN_GROUP or out["ratio"] is None:
        return out
    _attach_halves(out, a, b, stat)
    out["verdict"] = _decide(out)
    return out


# ---------------------------------------------------------------------------------------------------------------
# Records, exclusions, tables, GA4 and the report.
# ---------------------------------------------------------------------------------------------------------------

FEATURE_KEYS = ("kind", "news", "content_type", "topic_group", "slot", "planned_hour", "day_posts", "series_order",
                "card_h1", "lead")
LABEL_KEYS = ("hook_number", "hook_reframe", "person_role")
GA4_LINKEDIN_SOURCE = re.compile(r"linkedin|lnkd", re.IGNORECASE)
GA4_PATH = re.compile(r"^/(?:posts|toolset)/([a-z0-9-]+)/?$")
GA4_COLUMN_NAMES = {"page": ("landing page", "strona docelowa"), "date": ("date", "data"),
                    "sessions": ("sessions", "sesje")}
GA4_DISPLAY_NAMES = {"page": "Landing page", "date": "Date", "sessions": "Sessions"}
GA4_SOURCE_WORDS = ("source", "\u017ar\u00f3d\u0142o", "zrodlo")   # English and Polish column names
GA4_NEEDS_LINKEDIN = ("needs LinkedIn-filtered GA4: this file counts every source, and the registered metric "
                      "is LinkedIn sessions")
FACTORS = ("kind", "news", "content_type", "topic_group", "slot", "series", "hook_number", "hook_reframe",
           "person_role", "weekday", "planned_hour")


def exclusion_reason(rec: dict, export_date: str) -> str:
    if rec["disturbance"] or rec["sent"] in DISTURBANCES:
        return "disturbed"
    if rec["multi_send"] == "1":
        return "multi_send"
    return "immature" if _days_apart(export_date, rec["sent"]) < MATURITY_DAYS else ""


def _site_per_1000(rec: dict, ga4) -> float | None:
    if ga4 is None:
        return None
    start = date.fromisoformat(rec["sent"])
    days = {(start + timedelta(days=n)).isoformat() for n in range(FIRST_DAYS)}
    sessions = sum(v for day, v in ga4.get(rec["slug"], {}).items() if day in days)
    return sessions / rec["impressions"] * 1000 if rec["impressions"] else None


def _record(row, feat, label, export_date):
    rec = {"slug": row["slug"], "sent": row["created"], "multi_send": row["multi_send"],
           "disturbance": feat["disturbance"], "pub": feat["date"], **{k: feat[k] for k in FEATURE_KEYS},
           **{k: label.get(k, "") for k in LABEL_KEYS}, **{k: int(row[k]) for k in LINKEDIN_NUMBERS}}
    rec["series"] = "series" if rec["series_order"] else "standalone"
    rec["weekday"] = date.fromisoformat(rec["sent"]).strftime("%A")
    rec["excluded"] = exclusion_reason(rec, export_date)
    return rec


def _annotate_one(rec, comparable, typical, ga4):
    if rec["excluded"]:
        rec.update({"imp_index": None, "outlier": False, "site_per_1000": None})
        return
    rec["imp_index"] = imp_index(rec, comparable)
    rec["outlier"] = bool(typical) and rec["impressions"] > OUTLIER_MULTIPLE * typical
    rec["site_per_1000"] = _site_per_1000(rec, ga4)


def _annotate(recs, ga4):
    comparable = [r for r in recs if not r["excluded"]]
    typical = median([r["impressions"] for r in comparable])
    for rec in recs:
        _annotate_one(rec, comparable, typical, ga4)


def build_records(rows, feats, labels, export_date, ga4):
    recs = [_record(row, feats[row["slug"]], labels.get(row["slug"], {}), export_date) for row in rows if row["slug"]]
    _annotate(recs, ga4)
    return recs


def _rate(rows, numerator):
    impressions = sum(r["impressions"] for r in rows)
    return 1000 * sum(numerator(r) for r in rows) / impressions if impressions else None


def factor_table(rows, key):
    groups: dict = {}
    for row in rows:
        groups.setdefault(str(row[key]), []).append(row)
    table = []
    for group, members in sorted(groups.items()):
        q1, q3 = quartiles([r["imp_index"] for r in members if r.get("imp_index") is not None])
        table.append({
            "group": group, "n": len(members), "median_imp_index": median_of("imp_index")(members), "q1": q1, "q3": q3,
            "median_impressions": median([r["impressions"] for r in members]),
            "comment_repost_per_1000": _rate(members, lambda r: r["comments"] + r["reposts"]),
            "clicks_per_1000": _rate(members, lambda r: r["clicks"]),
            "reactions_reposts_per_1000": _rate(members, lambda r: r.get("reactions", 0) + r["reposts"]),
            "share_with_comment": sum(r["comments"] + r["reposts"] > 0 for r in members) / len(members)})
    return table


def _slug_of_path(landing: str) -> str:
    path = re.sub(r"^https?://[^/]+", "", landing.strip()).split("?")[0].split("#")[0].lower()
    match = GA4_PATH.match(path)
    return match.group(1) if match else ""


def _ga4_day(text: str) -> str:
    text = text.strip()
    if re.fullmatch(r"\d{8}", text):
        return f"{text[:4]}-{text[4:6]}-{text[6:]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text
    raise ExportError(f"GA4 date {text!r} is neither YYYYMMDD nor YYYY-MM-DD")


def _ga4_lines(path: Path) -> list[str]:
    return [ln for ln in path.read_text(encoding="utf-8-sig").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")]


def _ga4_find(fields, names, exact):
    for field in fields:
        low = field.lower()
        if (low in names) if exact else low.startswith(names):
            return field
    return None


def _ga4_columns(path: Path, fields: list[str]) -> dict:
    found = {"page": _ga4_find(fields, GA4_COLUMN_NAMES["page"], exact=False),
             "date": _ga4_find(fields, GA4_COLUMN_NAMES["date"], exact=True),
             "sessions": _ga4_find(fields, GA4_COLUMN_NAMES["sessions"], exact=True)}
    missing = [GA4_DISPLAY_NAMES[name] for name, column in found.items() if not column]
    if missing:
        raise ExportError(f"{path.name}: missing column(s) {missing}; found {fields}")
    found["source"] = next((f for f in fields if any(word in f.lower() for word in GA4_SOURCE_WORDS)), None)
    return found


def _ga4_add(out: dict, row: dict, cols: dict) -> None:
    slug = _slug_of_path(row[cols["page"]])
    if slug:
        days = out.setdefault(slug, {})
        day = _ga4_day(row[cols["date"]])
        days[day] = days.get(day, 0) + int(row[cols["sessions"]].replace(",", "") or 0)


def read_ga4_landing_by_date(path: Path) -> dict:
    """Sessions per post per day. Comment lines start with #; a source column, if present, selects LinkedIn."""
    reader = csv.DictReader(_ga4_lines(path))
    cols = _ga4_columns(path, reader.fieldnames or [])
    out: dict = {}
    for row in reader:
        if not cols["source"] or GA4_LINKEDIN_SOURCE.search(row[cols["source"]]):
            _ga4_add(out, row, cols)
    return out


def _ga4_header_and_preamble(path: Path) -> tuple[str, str]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    header = next((ln for ln in lines if ln.strip() and not ln.startswith("#")), "")
    return header.lower(), "\n".join(ln for ln in lines if ln.startswith("#"))


def ga4_scope(path: Path) -> str:
    """'linkedin' if the file splits by source or names LinkedIn in its preamble; otherwise every source is mixed."""
    header, preamble = _ga4_header_and_preamble(path)
    split_by_source = any(word in header for word in GA4_SOURCE_WORDS)
    return "linkedin" if split_by_source or GA4_LINKEDIN_SOURCE.search(preamble) else "all-sources"


def _usable(pool, metric):
    needs = {"imp_index": "imp_index", "site_sessions_per_1000": "site_per_1000"}.get(metric)
    return [r for r in pool if r[needs] is not None] if needs else list(pool)


def _judge_pool(spec, pool):
    usable = _usable(pool, spec["metric"])
    a = [r for r in usable if spec["in_a"](r)]
    b = [r for r in usable if not spec["in_a"](r)]
    return judge(a, b, stat_for(spec["metric"]), a + b)


def _site_blocked(spec, scope):
    """Why the site metric cannot give a verdict, or an empty string."""
    if spec["metric"] != "site_sessions_per_1000":
        return ""
    if scope is None:
        return "needs GA4: no GA4 file"
    return "" if scope == "linkedin" else GA4_NEEDS_LINKEDIN


def _hypothesis_row(name, spec, comparable, scope):
    row = {"id": name, "claim": spec["claim"], "metric": spec["metric"]}
    blocked = _site_blocked(spec, scope)
    if scope is None and blocked:
        return {**row, "verdict": blocked}
    for label, pool in (("", comparable), ("_no_outliers", [r for r in comparable if not r["outlier"]])):
        row.update({f"{k}{label}": v for k, v in _judge_pool(spec, pool).items()})
    if blocked:
        row["verdict"] = row["verdict_no_outliers"] = f"{blocked} (numbers are descriptive only)"
    return row


def verdict_rows(records, scope) -> list[dict]:
    comparable = [r for r in records if not r["excluded"]]
    return [_hypothesis_row(name, spec, comparable, scope) for name, spec in HYPOTHESES.items()]


def _cadence_labels(rec):
    labels = []
    if rec["slot"] == "1":
        labels.append("first")
    if rec["slot"] == "1" and int(rec["day_posts"]) >= 2:
        labels.append("first_double")
    if rec["slot"] == "2":
        labels.append("second")
    if int(rec["day_posts"]) == 1:
        labels.append("single")
    return labels


def _cadence_eligible(rec):
    return not rec["excluded"] and rec["imp_index"] is not None and rec["sent"] >= CADENCE_FROM


def _slot_views(records):
    groups: dict = {}
    for rec in filter(_cadence_eligible, records):
        for label in _cadence_labels(rec):
            groups.setdefault(label, []).append(rec)
    index = median_of("imp_index")

    def view(title, a, b):
        return (title, len(groups.get(a, [])), index(groups.get(a, [])), len(groups.get(b, [])), index(groups.get(b, [])))
    return [view("first slot on a double day vs a single-post day (imp_index)", "first_double", "single"),
            view("second slot vs first slot (imp_index)", "second", "first")]


def _impressions_by_day(daily):
    return {datetime.strptime(d["Date"], LINKEDIN_DATE_FORMAT).date().isoformat(): int(float(d["Impressions (total)"]))
            for d in daily}


def _daily_view(records, daily):
    per_day: dict = {}
    for rec in records:
        per_day[rec["sent"]] = per_day.get(rec["sent"], 0) + 1
    recent = {day: total for day, total in _impressions_by_day(daily).items() if day >= CADENCE_FROM}
    double = [total for day, total in recent.items() if per_day.get(day, 0) >= 2]
    single = [total for day, total in recent.items() if per_day.get(day, 0) == 1]
    return ("total impressions per day, double-post days vs single-post days", len(double), median(double),
            len(single), median(single))


def cadence_views(records, daily):
    return [*_slot_views(records), _daily_view(records, daily)]


def registered_values_match(doc: Path) -> list[str]:
    block = re.search(r"<!-- preregistration:start -->\n(.*?)\n<!-- preregistration:end -->", doc.read_text(), re.DOTALL)
    if not block:
        return ["the registered-values block is missing"]
    wrong = []
    for line in block.group(1).splitlines():
        name, _, value = line.partition(" = ")
        mine = PRIMARY_METRICS.get(name) if name in HYPOTHESES else globals().get(name)
        if str(mine) != value:
            wrong.append(f"{name}: doc {value!r}, script {mine!r}")
    return wrong


def _fmt(value, digits=2):
    return "n/a" if value is None else f"{value:.{digits}f}"


def _verdict_table(rows) -> list[str]:
    lines = ["| # | claim | metric | n A / B | A, B | ratio | verdict | without outliers |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if "n_a" not in r:
            lines.append(f"| {r['id']} | {r['claim']} | {r['metric']} | | | | {r['verdict']} | |")
            continue
        lean = f" (leans {r['lean']})" if r["verdict"] == "too little data" and r["lean"] else ""
        lines.append(f"| {r['id']} | {r['claim']} | {r['metric']} | {r['n_a']} / {r['n_b']} | {_fmt(r['stat_a'])}, "
                     f"{_fmt(r['stat_b'])} | {_fmt(r['ratio'])} | {r['verdict']}{lean} | {r['verdict_no_outliers']} |")
    return lines


def _factor_lines(records) -> list[str]:
    comparable = [r for r in records if not r["excluded"]]
    lines = []
    for key in FACTORS:
        for label, pool in (("all compared posts", comparable), ("without outliers", [r for r in comparable if not r["outlier"]])):
            lines += [f"### {key}, {label}", "", "| group | n | median index | Q1-Q3 | median impressions | comments+reposts/1000 | clicks/1000 | share with a comment |",
                      "|---|---|---|---|---|---|---|---|"]
            lines += [f"| {t['group']} | {t['n']} | {_fmt(t['median_imp_index'])} | {_fmt(t['q1'])}-{_fmt(t['q3'])} | "
                      f"{_fmt(t['median_impressions'], 0)} | {_fmt(t['comment_repost_per_1000'])} | {_fmt(t['clicks_per_1000'])} | "
                      f"{t['share_with_comment']:.0%} |" for t in factor_table(pool, key)] + [""]
    return lines


def _placebo_line(records) -> str:
    comparable = [r for r in records if not r["excluded"] and r["imp_index"] is not None]
    return f"Placebo (even against odd calendar day, median index): noise floor ratio {_fmt(noise_floor(median_of('imp_index'), comparable))}"


def _head(ctx) -> list[str]:
    recs = ctx["records"]
    reasons = {k: sum(r["excluded"] == k for r in recs) for k in ("disturbed", "multi_send", "immature")}
    return [f"pre-registration commit: {ctx['registered_at']}", f"labels sha256: {ctx['labels_sha']}",
            f"export date: {ctx['export_date']}; LinkedIn rows placed on posts: {len(recs)}",
            f"compared: {sum(not r['excluded'] for r in recs)}; listed but not compared: {reasons}",
            f"outliers (above {OUTLIER_MULTIPLE}x the median impressions): {sum(r['outlier'] for r in recs)}"]


def render_summary(ctx) -> str:
    """Aggregates only: no post is named, so this file is the one that could be shared."""
    lines = ["# Social review: summary (aggregates only)", "", *_head(ctx), "", "## Verdicts (registered rule)", "",
             *_verdict_table(ctx["verdicts"]), "", "## Cadence and timing (descriptive; confounded, no verdict)", "",
             "| view | n A | median A | n B | median B |", "|---|---|---|---|---|"]
    lines += [f"| {v[0]} | {v[1]} | {_fmt(v[2], 0 if v[2] and v[2] > 50 else 2)} | {v[3]} | {_fmt(v[4], 0 if v[4] and v[4] > 50 else 2)} |"
              for v in ctx["cadence"]]
    return "\n".join([*lines, "", _placebo_line(ctx["records"]), "", "## Factors", "", *_factor_lines(ctx["records"])]) + "\n"


def _describe(rec) -> str:
    hooks = [name for name in ("hook_number", "hook_reframe") if rec[name] == "yes"]
    return ", ".join([rec["kind"], "news" if rec["news"] == "1" else "evergreen", rec["content_type"], rec["topic_group"], *hooks])


def render_report(ctx) -> str:
    """Private: names every post, so it stays in the ignored data folder."""
    ranked = sorted([r for r in ctx["records"] if r["imp_index"] is not None], key=lambda r: r["imp_index"])
    row = lambda r: f"| {r['slug']} | {r['sent']} | {_fmt(r['imp_index'])} | {r['impressions']} | {_describe(r)} |"
    head = ["| post | sent | index | impressions | what it is |", "|---|---|---|---|---|"]
    lines = ["# Social review: per-post report (private)", "", *_head(ctx), "", "## Top and bottom by impressions index", "",
             *head, *[row(r) for r in ranked[::-1][:TOP_N]], "", "bottom:", "", *head, *[row(r) for r in ranked[:TOP_N]], "",
             "## Not compared", "", *[f"- {r['slug']}: {r['excluded']}" for r in ctx["records"] if r["excluded"]]]
    return "\n".join(lines) + "\n"


POSTS_COLUMNS = ("slug", "sent", "excluded", "outlier", "imp_index", "impressions", "clicks", "reactions", "comments",
                 "reposts", "site_per_1000", "kind", "news", "content_type", "topic_group", "slot", "hook_number",
                 "hook_reframe", "person_role", "card_h1")


def _context(folder: Path, args) -> dict:
    ga4_path = Path(args.ga4) if args.ga4 else folder / "ga4-linkedin-landing-by-date.csv"
    ga4 = read_ga4_landing_by_date(ga4_path) if ga4_path.exists() else None
    scope = ga4_scope(ga4_path) if ga4 is not None else None
    joined = _read_csv(folder / "joined.csv")
    records = build_records(joined, {r["slug"]: r for r in _read_csv(folder / "features.csv")},
                            {r["slug"]: r for r in _read_csv(folder / "labels.csv")}, args.export_date, ga4)
    daily_path = folder / "linkedin-daily.csv"
    return {"records": records, "verdicts": verdict_rows(records, scope), "export_date": args.export_date,
            "cadence": cadence_views(records, _read_csv(daily_path) if daily_path.exists() else []),
            "registered_at": _git(REPO, "log", "-1", "--format=%H", "--", "docs/analytics.md") or "unknown",
            "labels_sha": hashlib.sha256((folder / "labels.csv").read_bytes()).hexdigest(), "ga4_scope": scope}


def cmd_report(args: argparse.Namespace) -> int:
    folder = Path(args.dir)
    if not is_safe_to_write(folder / "report.md"):
        print(f"refusing to write in {folder}: git does not ignore it, and the repository is public", file=sys.stderr)
        return EXIT_NOT_IGNORED
    drift = registered_values_match(REPO / "docs" / "analytics.md")
    if drift:
        print("the registered values differ from the script, so no verdict is valid: " + "; ".join(drift), file=sys.stderr)
        return EXIT_UNRESOLVED
    if not (folder / "joined.csv").exists() or any(not r["slug"] and not r["method"] for r in _read_csv(folder / "joined.csv")):
        print("joined.csv is missing or has unplaced rows: run the join first", file=sys.stderr)
        return EXIT_UNRESOLVED
    try:
        ctx = _context(folder, args)
    except ExportError as error:
        print(f"export problem: {error}", file=sys.stderr)
        return EXIT_UNRESOLVED
    (folder / "summary.md").write_text(render_summary(ctx), encoding="utf-8")
    (folder / "report.md").write_text(render_report(ctx), encoding="utf-8")
    _write_dicts(folder / "posts.csv", ctx["records"], POSTS_COLUMNS)
    print("\n".join([*_head(ctx), *_verdict_table(ctx["verdicts"])]))
    return 0


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
    report = sub.add_parser("report", help="tables and the registered verdicts, from the joined data")
    report.add_argument("--dir", required=True)
    report.add_argument("--export-date", required=True, help="YYYY-MM-DD the LinkedIn export was taken")
    report.add_argument("--ga4", help="GA4 landing-page-by-date CSV; defaults to the file in --dir")
    args = parser.parse_args(argv)
    return {"join": cmd_join, "report": cmd_report}.get(args.command, cmd_features)(args)


if __name__ == "__main__":
    sys.exit(main())
