#!/usr/bin/env python3
"""Lint wro.cpp prose for AI-writing tells (house style: docs/STYLE.md).

The linter masks code / frontmatter / JSX props / tables / links first, then
checks the resulting "prose view" against budgets for our recurring tells:
dashes, formulaic closers, negative parallelism, punchy fragments,
significance-inflation, colon-title formula, generic section headers,
rule-of-three anaphora, bold overuse, and skeleton openers.

It is a gate, not a substitute for the human read. Some tells (the
myth->demo->catch->teaser skeleton, whether adjectives are earned) are not
mechanically checkable and are left to docs/STYLE.md + human review.

Usage:
  scripts/prose-lint.py --slug erroneous-behavior        # one post: body + title
  scripts/prose-lint.py --file src/content/posts/X.mdx   # arbitrary .mdx
  scripts/prose-lint.py --caption social/linkedin/S/caption.md
  scripts/prose-lint.py --slug S --caption-check         # post + both captions
  scripts/prose-lint.py --all                            # corpus stats (advisory)
  scripts/prose-lint.py --slug S --strict                # promote every WARN to ERROR

Readability (docs/STYLE.md, "Readability"): sentence-length, code-density, paragraph,
prose-run, section-length and in-short. They see inline code spans. A post listed in
scripts/readability-baseline.json is only reported where it is WORSE than its entry; a post
that is not listed is fully enforced. Captions are not affected.

Exit code: 0 = clean (WARN allowed), 1 = at least one ERROR, 2 = usage / not found.
"""

import argparse
import glob
import importlib.util
import re
import sys
from pathlib import Path

YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
DIM = "\033[2m"
RESET = "\033[0m"

# --- budgets (body unless noted); see docs/STYLE.md -----------------------
DASH_WARN = 2        # WARN when body double-dash/em-dash count exceeds this
DASH_ERROR = 4       # ERROR when it exceeds this
NEGPAR_ERROR = 2     # ERROR at this many negative-parallelism hits
ANAPHORA_ERROR = 2
GENERIC_HEADER_ERROR = 2
BOLD_WARN = 8
BOLD_ERROR = 14

CLOSER_RE = re.compile(
    r"that('?s| is) the (whole |entire )?point"
    r"|the (whole|entire) point\b"
    r"|that('?s| is) the payoff"
    r"|worth remembering"
    r"|sharp edges?\b[^.]{0,20}\bdocumented",
    re.IGNORECASE,
)
NEGPAR_RE = re.compile(
    r"\bnot (a|an|just|only|about|the)\b[^.,;]{1,45},\s*(it('?s| is)|but)\b"
    r"|\bis not just\b[^.,;]{1,35},\s*it\b"
    r"|\bwith (better|extra) (marketing|steps)\b",
    re.IGNORECASE,
)
SIGNIF_RE = re.compile(
    r"\bthe strongest\b"
    r"|closest to home"
    r"|matters most\b"
    r"|worth more than one post"
    r"|the part most\b"
    r"|most (introductions|people|posts|guides|tutorials) (skip|miss|gloss|leave out)",
    re.IGNORECASE,
)
SKELETON_RE = re.compile(
    r"usually pitched as"
    r"|we are trained to expect"
    r"|you('?d| would) expect"
    r"|with better marketing",
    re.IGNORECASE,
)
CAPTION_TIC_RE = re.compile(r"\blive in your browser\b|\bfull stop\b", re.IGNORECASE)
GENERIC_HEADER_RE = re.compile(
    r"^#{2,4}\s+(why (it|this) matters"
    r"|what this means( for .+)?"
    r"|what'?s next"
    r"|the catch(,.*)?"
    r"|the payoff"
    r"|takeaways?"
    r"|conclusion"
    r"|tl;?dr)\s*$",
    re.IGNORECASE,
)
COLON_TITLE_RE = re.compile(r":\s+the\b.+\bthat\b", re.IGNORECASE)
DASH_RE = re.compile(r"(?<!-)--(?!-)")
ANAPHORA_RE = re.compile(
    r"\b(\w+)\s+\w+,\s+\1\s+\w+,\s+\1\s+\w+"  # "same X, same Y, same Z"
    r"|\bno\s+\w+,\s+no\s+\w+,\s+no\s+\w+",
    re.IGNORECASE,
)
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*|(?<!_)__[^_\n]+__(?!_)")


def mask_prose(text: str):
    """Return a list of (lineno, masked_line). Regions that must never be seen
    by a tell check are blanked (replaced with spaces so columns line up):
    YAML frontmatter, fenced code, inline `code`, <JSX .../> tags, markdown
    table separator rows, link URL targets, and import lines."""
    lines = text.split("\n")
    out = []
    in_fence = False
    fence_marker = ""
    seen_frontmatter_open = False
    in_frontmatter = False
    for idx, raw in enumerate(lines, start=1):
        line = raw

        # YAML frontmatter: first --- opens, next --- closes.
        stripped = line.strip()
        if stripped == "---" and not seen_frontmatter_open and idx <= 3:
            seen_frontmatter_open = True
            in_frontmatter = True
            out.append((idx, ""))
            continue
        if in_frontmatter:
            out.append((idx, ""))
            if stripped == "---":
                in_frontmatter = False
            continue

        # Fenced code blocks (``` or ~~~).
        fence_m = re.match(r"^(\s*)(`{3,}|~{3,})", line)
        if fence_m:
            marker = fence_m.group(2)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
                out.append((idx, ""))
                continue
            elif marker == fence_marker:
                in_fence = False
                out.append((idx, ""))
                continue
        if in_fence:
            out.append((idx, ""))
            continue

        # Import lines.
        if re.match(r"^\s*import\b.*\bfrom\b", line):
            out.append((idx, ""))
            continue

        # Markdown table separator rows: | --- | :--: | etc.
        if re.match(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$", line):
            out.append((idx, ""))
            continue

        # Blank inline code, JSX tags, and link URL targets (keep link text).
        line = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        line = re.sub(r"<[^>]*>", lambda m: " " * len(m.group(0)), line)
        line = re.sub(r"\]\([^)]*\)", lambda m: "]" + " " * (len(m.group(0)) - 1), line)

        out.append((idx, line))
    return out


def extract_title(text: str):
    m = re.search(r'^title:\s*["\'](.+?)["\']', text, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip().strip("\"'") if m else None


def level_for(count, warn_at, error_at):
    if count > error_at:
        return "ERROR"
    if count > warn_at:
        return "WARN"
    return None


def body_prose_lines(masked):
    """Prose lines suitable for sentence-level checks: drop headings, list
    items, blockquotes, table rows, and blanks."""
    keep = []
    for lineno, line in masked:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith(">"):
            continue
        if re.match(r"^([-*+]|\d+\.)\s", s):
            continue
        if s.startswith("|"):
            continue
        keep.append((lineno, line))
    return keep


def check_punchy(masked):
    """Runs of >=2 adjacent sentences each <=4 words."""
    prose = body_prose_lines(masked)
    text = " ".join(l for _, l in prose)
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    runs, cur = [], 0
    for s in sentences:
        words = len(re.findall(r"[A-Za-z0-9']+", s))
        if 0 < words <= 4:
            cur += 1
        else:
            if cur >= 2:
                runs.append(cur)
            cur = 0
    if cur >= 2:
        runs.append(cur)
    return runs


def lint_body(text: str, label: str, strict: bool):
    """Return list of (level, message). label is used in output only."""
    masked = mask_prose(text)
    title = extract_title(text) or ""
    issues = []

    def add(level, tell, msg, lineno=None):
        loc = f":{lineno}" if lineno else ""
        issues.append((level, f"{tell}{loc}: {msg}"))

    joined = "\n".join(l for _, l in masked)

    # 1. Dashes (em/en dash chars + word/space-bounded double hyphens).
    dash_count = joined.count("—") + joined.count("–") + len(DASH_RE.findall(joined))
    lvl = level_for(dash_count, DASH_WARN, DASH_ERROR)
    if lvl:
        add(lvl, "dashes", f"{dash_count} dash asides (budget {DASH_WARN}); convert to periods/parens")

    # 2. Formulaic closers (closing zone + title).
    prose = body_prose_lines(masked)
    zone = prose[-6:]
    for lineno, line in zone:
        if CLOSER_RE.search(line):
            add("ERROR", "closer", f"formulaic sign-off: {line.strip()[:70]!r}", lineno)
    if CLOSER_RE.search(title):
        add("ERROR", "closer", f"formulaic phrase in TITLE: {title!r}")

    # 3. Negative parallelism.
    neg = 0
    for lineno, line in masked:
        for _ in NEGPAR_RE.finditer(line):
            neg += 1
            add("WARN", "neg-parallel", f"'not X, it/but Y': {line.strip()[:70]!r}", lineno)
    if neg >= NEGPAR_ERROR:
        add("ERROR", "neg-parallel", f"{neg} negative-parallelism constructions (keep <=1)")

    # 4. Punchy-fragment runs.
    runs = check_punchy(masked)
    if any(r >= 3 for r in runs) or len(runs) > 1:
        add("WARN", "fragments", f"staccato fragment run(s) of length {runs}; keep to one short beat")
    for lineno, line in masked:
        if CAPTION_TIC_RE.search(line):
            add("WARN", "tic", f"stock phrase: {line.strip()[:60]!r}", lineno)

    # 5. Significance-inflation.
    for lineno, line in masked:
        if SIGNIF_RE.search(line):
            add("WARN", "significance", f"narrator importance-claim: {line.strip()[:70]!r}", lineno)

    # 6. Skeleton openers.
    for lineno, line in masked:
        if SKELETON_RE.search(line):
            add("WARN", "skeleton", f"stock opener: {line.strip()[:70]!r}", lineno)

    # 7. Colon-title formula.
    if COLON_TITLE_RE.search(title):
        add("WARN", "colon-title", f"'X: the Y that Z' formula: {title!r}")

    # 8. Generic section headers.
    generic = 0
    for lineno, line in masked:
        if GENERIC_HEADER_RE.match(line.strip()):
            generic += 1
            add("WARN", "generic-header", f"name the section by its content: {line.strip()!r}", lineno)
    if generic >= GENERIC_HEADER_ERROR:
        add("ERROR", "generic-header", f"{generic} generic headers (Why it matters / What's next / The catch)")

    # 9. Rule-of-three anaphora.
    ana = 0
    for lineno, line in masked:
        for _ in ANAPHORA_RE.finditer(line):
            ana += 1
            add("WARN", "anaphora", f"tricolon anaphora: {line.strip()[:70]!r}", lineno)
    if ana >= ANAPHORA_ERROR:
        add("ERROR", "anaphora", f"{ana} rule-of-three anaphora constructions (keep <=1)")

    # 10. Bold overuse.
    bold_count = len(BOLD_RE.findall(joined))
    lvl = level_for(bold_count, BOLD_WARN, BOLD_ERROR)
    if lvl:
        add(lvl, "bold", f"{bold_count} bold spans (budget {BOLD_WARN}); bold only term-of-art intros")

    # 11. Readability (keeps inline code spans; grandfathered by the baseline).
    issues.extend(readability_issues(text))

    if strict:
        issues = [("ERROR" if lv == "WARN" else lv, m) for lv, m in issues]
    return issues


# --- readability pass (spans kept; numbers live in readability-report.py) ----

def _load_report():
    path = Path(__file__).resolve().parent / "readability-report.py"
    spec = importlib.util.spec_from_file_location("readability_report", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# (tell, level, metric key, detail builder name, message). A rule is active when the
# post's metric is above its baseline entry (0 when the post is not in the baseline).
READABILITY_RULES = [
    ("sentence-length", "ERROR", "n_over35", "sent_error"),
    ("sentence-length", "WARN", "n_over25", "sent_warn"),
    ("sentence-length", "WARN", "n_sec_mean20", "section_mean"),
    ("code-density", "ERROR", "n_sent_spans_gt4", "spans_error"),
    ("code-density", "WARN", "n_sent_spans_gt2", "spans_warn"),
    ("code-density", "WARN", "dense_excess", "dense"),
    ("paragraph", "ERROR", "n_para_over7", "para_sentences"),
    ("paragraph", "WARN", "n_para_over120", "para_words"),
    ("prose-run", "WARN", "n_runs_over4", "runs"),
    ("section-length", "WARN", "n_sec_over300", "section_words"),
    ("in-short", "WARN", "no_in_short", "in_short"),
]


def _snip(row):
    return row["text"][:70] + ("..." if len(row["text"]) > 70 else "")


def _sentence_items(rows, lo, hi):
    return [(r["line"], f"{r['n']} words (limit {lo}): {_snip(r)!r}")
            for r in rows if lo < r["n"] <= hi]


def _span_items(rows, lo, hi):
    return [(r["line"], f"{r['spans']} code spans in one sentence (limit {lo}): {_snip(r)!r}")
            for r in rows if lo < r["spans"] <= hi]


def readability_details(rep, metrics, detail):
    """Line-numbered findings per rule key; each value is a list of (lineno|None, message)."""
    rows, big = detail["rows"], 10 ** 6
    secs = detail["secs"]
    out = {
        "sent_error": _sentence_items(rows, rep.SENT_ERROR, big),
        "sent_warn": _sentence_items(rows, rep.SENT_WARN, rep.SENT_ERROR),
        "spans_error": _span_items(rows, rep.SPANS_SENT_ERROR, big),
        "spans_warn": _span_items(rows, rep.SPANS_SENT_WARN, rep.SPANS_SENT_ERROR),
        "dense": [(None, f"{metrics['spans_per100']} code spans per 100 prose words (limit {rep.SPANS_PER100_WARN}); "
                         "name the thing in words, keep inline code for single names")],
        "para_sentences": [(p["line"], f"paragraph of {p['sents']} sentences (limit {rep.PARA_SENT_ERROR})")
                           for p in detail["paras"] if p["sents"] > rep.PARA_SENT_ERROR],
        "para_words": [(p["line"], f"paragraph of {p['words']} words (limit {rep.PARA_WORDS_WARN})")
                       for p in detail["paras"] if p["words"] > rep.PARA_WORDS_WARN],
        "runs": [(None, f"{metrics['n_runs_over4']} stretch(es) of more than {rep.RUN_WARN} prose paragraphs "
                        f"without a heading, list, table, code block or embed (longest {metrics['max_prose_run']})")],
        "section_words": [(None, f"{metrics['n_sec_over300']} section(s) over {rep.SECTION_WORDS_WARN} prose words "
                                 f"(longest {metrics['max_section_words']}); add a heading")],
        "section_mean": [(None, f"{metrics['n_sec_mean20']} section(s) with mean sentence length over {rep.SENT_MEAN_MAX}")],
        "in_short": [(None, f"{metrics['words']} prose words and no 'In short' first section (3-5 bullets)")],
    }
    return out


def readability_issues(text, baseline=None):
    """Readability findings as (level, message). `baseline` maps slug -> metrics; a rule
    only fires for a listed post when its metric is worse than the baseline entry."""
    rep = _load_report()
    metrics, detail = rep.analyze(text)
    if baseline is None:
        baseline = rep.load_baseline()
    base = baseline.get(rep.post_slug("", detail["fields"]), {})
    details = readability_details(rep, metrics, detail)
    issues = []
    for tell, level, key, dkey in READABILITY_RULES:
        if metrics[key] <= base.get(key, 0):
            continue
        suffix = f" (baseline {base[key]})" if key in base else ""
        for lineno, msg in details[dkey]:
            loc = f":{lineno}" if lineno else ""
            issues.append((level, f"{tell}{loc}: {msg}{suffix}"))
    return issues


def lint_caption(path: Path, strict: bool):
    """Captions are stricter: zero dashes, no stock tics, no closers."""
    text = path.read_text(encoding="utf-8")
    # Only the ## Body section carries the human-visible prose.
    m = re.search(r"^##\s*Body\s*$(.*?)(^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    body = m.group(1) if m else text
    masked = mask_prose(body)
    joined = "\n".join(l for _, l in masked)
    issues = []

    dash_count = joined.count("—") + joined.count("–") + len(DASH_RE.findall(joined))
    if dash_count:
        issues.append(("ERROR", f"dashes: {dash_count} dash(es) in caption; captions use periods/parens, zero '--'"))
    if CAPTION_TIC_RE.search(joined):
        issues.append(("ERROR", "tic: stock caption phrase ('Live in your browser.' / 'full stop')"))
    if CLOSER_RE.search(joined):
        issues.append(("ERROR", "closer: formulaic sign-off; end on the claim + the link"))
    neg = len(NEGPAR_RE.findall(joined))
    if neg >= 2:
        issues.append(("ERROR", f"neg-parallel: {neg} 'not X, it Y' constructions (keep <=1)"))
    elif neg == 1:
        issues.append(("WARN", "neg-parallel: one 'not X, it Y' (only for a real misconception)"))
    if strict:
        issues = [("ERROR" if lv == "WARN" else lv, m) for lv, m in issues]
    return issues


def resolve_slug(root: Path, slug: str):
    hits = sorted(root.glob(f"src/content/posts/*-{slug}.mdx"))
    if hits:
        return hits[0]
    # Fall back to the frontmatter `slug:` field (some posts have a filename
    # that differs from their slug, e.g. ai-cpp-workflow.mdx -> ai-cpp-workflow-2026).
    for p in sorted(root.glob("src/content/posts/*.mdx")):
        m = re.search(r'^slug:\s*["\']?(.+?)["\']?\s*$', p.read_text(encoding="utf-8"), re.MULTILINE)
        if m and m.group(1).strip() == slug:
            return p
    return None


def emit(label, issues):
    has_error = False
    if not issues:
        print(f"{GREEN}OK{RESET}    {label}")
        return False
    print(f"{label}:")
    for lv, msg in issues:
        color = RED if lv == "ERROR" else YELLOW
        print(f"  {color}{lv:5}{RESET} {msg}")
        if lv == "ERROR":
            has_error = True
    return has_error


def print_legend():
    print()
    print(f"{DIM}budgets: dashes<=2  closers=0  neg-parallel<=1  generic-headers=0")
    print(f"         anaphora<=1  bold<=8  captions: zero dashes/tics/closers")
    print(f"         see docs/STYLE.md; some tells (skeleton, earned adjectives) are human-review{RESET}")


def run_all(root: Path, strict: bool = False):
    posts = sorted(root.glob("src/content/posts/*.mdx"))
    total_dash = 0
    colon_the = 0
    with_error = 0
    for p in posts:
        text = p.read_text(encoding="utf-8")
        masked = mask_prose(text)
        joined = "\n".join(l for _, l in masked)
        d = joined.count("—") + joined.count("–") + len(DASH_RE.findall(joined))
        total_dash += d
        title = extract_title(text) or ""
        if re.search(r"\S\s*:\s+the\b", title, re.IGNORECASE):
            colon_the += 1
        issues = lint_body(text, p.stem, strict=False)
        if any(lv == "ERROR" for lv, _ in issues):
            with_error += 1
    n = len(posts)
    print(f"corpus: {n} posts")
    print(f"  double-dash/em-dash asides (masked prose): {total_dash}")
    ratio = (100 * colon_the / n) if n else 0
    print(f"  ': the ...' titles: {colon_the}/{n} ({ratio:.0f}%; target < 25%)")
    print(f"  posts with >=1 ERROR-level tell: {with_error}/{n}")
    if strict:
        if with_error:
            print(f"{RED}gate: {with_error} post(s) carry an ERROR-level tell; run prose-lint.py --slug <slug> to see them.{RESET}")
            return 1
        print(f"{GREEN}gate: all {n} posts clean.{RESET}")
        return 0
    print(f"{DIM}(advisory sweep; exits 0. Add --strict to gate the build on ERROR-level tells.){RESET}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", help="lint src/content/posts/*-<slug>.mdx (body + title)")
    parser.add_argument("--file", type=Path, help="lint an arbitrary .mdx file")
    parser.add_argument("--caption", type=Path, help="lint a social caption.md (stricter)")
    parser.add_argument("--caption-check", action="store_true", help="with --slug: also lint both platform captions")
    parser.add_argument("--all", action="store_true", help="advisory corpus stats")
    parser.add_argument("--strict", action="store_true", help="promote every WARN to ERROR")
    args = parser.parse_args()

    root = Path(".")
    has_error = False
    did_something = False

    if args.all:
        sys.exit(run_all(root, args.strict))

    if args.caption:
        did_something = True
        if not args.caption.exists():
            print(f"{RED}ERROR{RESET} caption not found: {args.caption}")
            sys.exit(2)
        has_error |= emit(str(args.caption), lint_caption(args.caption, args.strict))

    target = None
    if args.file:
        target = args.file
    elif args.slug:
        target = resolve_slug(root, args.slug)
        if target is None:
            print(f"{RED}ERROR{RESET} no post found for slug {args.slug!r}")
            sys.exit(2)

    if target is not None:
        did_something = True
        if not target.exists() or target.suffix != ".mdx":
            print(f"{RED}ERROR{RESET} not an .mdx file: {target}")
            sys.exit(2)
        text = target.read_text(encoding="utf-8")
        has_error |= emit(target.stem, lint_body(text, target.stem, args.strict))

    if args.caption_check and args.slug:
        for plat in ("linkedin", "facebook"):
            cap = root / "social" / plat / args.slug / "caption.md"
            if cap.exists():
                did_something = True
                has_error |= emit(f"{plat}/{args.slug} caption", lint_caption(cap, args.strict))

    if not did_something:
        parser.print_help()
        sys.exit(2)

    print_legend()
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
