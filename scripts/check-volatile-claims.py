#!/usr/bin/env python3
"""Flag time-sensitive claims in posts that are about to publish.

Posts here are written days or weeks before they go out, and some of what they
say has a shelf life. On 2026-08-12 a post published saying a release candidate
was the newest when a later one had shipped; it was caught by luck during an
unrelated sweep. This finds those lines on purpose.

This is a REPORT, not a gate. It cannot know whether a claim is still true, only
that it is the kind of claim worth rechecking before publication.

Usage:
  scripts/check-volatile-claims.py                 # posts publishing in 14 days
  scripts/check-volatile-claims.py --days 7
  scripts/check-volatile-claims.py --all           # every future post
  scripts/check-volatile-claims.py --today 2026-08-16

Exit code is always 0 unless --strict, which fails when anything is flagged.
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = REPO / "src" / "content" / "posts"

# Each pattern is a claim shape whose truth changes without anyone editing the
# post. The comment says what actually goes stale.
PATTERNS = [
    # release candidates: superseded by the next rc or the final release
    (r"\brc\d\b|\brelease candidate\b", "release-candidate status"),
    # "not yet", "still at", "has not shipped": true until it is not
    (r"\b(?:still (?:at|on)|not yet (?:released|shipped|out)|has not (?:shipped|released)|no final release)\b",
     "not-yet-shipped claim"),
    # forecasts with a date attached
    (r"\b(?:expected|due|targeted|planned|scheduled|slated)\s+(?:for|in|on|to|by)\b|\blate (?:this )?(?:month|august|september|october|november|december)\b",
     "forecast date"),
    # superlatives about versions: a new release invalidates them
    (r"\b(?:newest|latest|current|most recent)\s+(?:release|version|stable)\b|\btops out at\b",
     "latest-version claim"),
    # explicit version-with-date assertions
    (r"\b\d+\.\d+(?:\.\d+)?\s+(?:is out|shipped|released|landed)\b", "dated release claim"),
    # counts that grow
    (r"\bso far\b|\bas of (?:today|writing|this week)\b", "as-of-writing claim"),
]

FENCE = re.compile(r"```.*?```", re.S)
FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.S)


def scan(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = re.search(r"^pubDate:\s*(\S+)", raw, re.M)
    if not m:
        return None, []
    pub = dt.date.fromisoformat(m.group(1).strip().strip('"'))

    # Search frontmatter summary AND body, but not fenced code (compiler output
    # legitimately contains version numbers and is not a claim being made).
    body = FRONTMATTER.sub("", raw)
    body = FENCE.sub("", body)
    summary = ""
    sm = re.search(r'^summary:\s*"(.*?)"\s*$', raw, re.M | re.S)
    if sm:
        summary = sm.group(1)

    hits = []
    for text, where in ((summary, "summary"), (body, "body")):
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pat, label in PATTERNS:
                if re.search(pat, line, re.I):
                    hits.append((where, label, line.strip()[:120]))
                    break
    return pub, hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--today", default=None, help="override today, YYYY-MM-DD")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    horizon = today + dt.timedelta(days=args.days)

    flagged = 0
    for path in sorted(POSTS.glob("*.mdx")):
        pub, hits = scan(path)
        if pub is None or not hits:
            continue
        if pub <= today:
            continue
        if not args.all and pub > horizon:
            continue
        days = (pub - today).days
        print(f"\n{path.name}  publishes in {days} day(s), {pub}")
        for where, label, line in hits:
            print(f"    [{label}] ({where}) {line}")
            flagged += 1

    print()
    if flagged:
        print(f"{flagged} claim(s) worth rechecking before publication.")
        print("None of these are necessarily wrong. Verify each against its source.")
    else:
        window = "any future post" if args.all else f"the next {args.days} days"
        print(f"No time-sensitive claims found in {window}.")

    return 1 if (flagged and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
