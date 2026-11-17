#!/usr/bin/env python3
"""Find days with no published post in the next few days.

The site promises at least one post a day. A day with none is a gap, and a gap that is found a week ahead can still be
filled. The daily scheduler runs this after it has queued posts; it prints the gaps, appends them to
.notes/radar-pending.md and raises a macOS notification.

  scripts/check_daily_gap.py                  # the 5 days after today (UTC)
  scripts/check_daily_gap.py --days 14        # look further ahead
  scripts/check_daily_gap.py --notify         # also notify (macOS) and append to .notes/radar-pending.md

Exit code: 0 = every day has a post, 1 = at least one gap.
"""

import argparse
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DAYS = 5
NOTES = REPO / ".notes" / "radar-pending.md"


def published_days(posts_dir: Path) -> set[str]:
    """Return the pubDate of every post that is not a draft."""
    days = set()
    for path in sorted(posts_dir.glob("*.mdx")):
        head = path.read_text().split("---")[1] if path.read_text().startswith("---") else ""
        match = re.search(r"^pubDate:\s*(\d{4}-\d{2}-\d{2})", head, re.M)
        draft = re.search(r"^draft:\s*true", head, re.M)
        if match and not draft:
            days.add(match.group(1))
    return days


def find_gaps(days_with_post: set[str], start: date, count: int) -> list[str]:
    window = [(start + timedelta(days=i)).isoformat() for i in range(count)]
    return [day for day in window if day not in days_with_post]


def notify(gaps: list[str]) -> None:
    text = "No post planned for: " + ", ".join(gaps)
    subprocess.run(
        ["osascript", "-e", f'display notification "{text}" with title "wro.cpp: gap in the post calendar"'],
        check=False,
    )
    NOTES.parent.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with NOTES.open("a") as handle:
        handle.write(f"- {stamp}: calendar gap, no post planned for {', '.join(gaps)}. Fill it or re-date a queued post.\n")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--root", type=Path, default=REPO)
    args = parser.parse_args(argv)

    tomorrow = datetime.now(timezone.utc).date() + timedelta(days=1)  # today's posts have already fired
    gaps = find_gaps(published_days(args.root / "src" / "content" / "posts"), tomorrow, args.days)
    if not gaps:
        print(f"OK: a post is planned on each of the next {args.days} days after today")
        return 0
    print(f"GAP: no post planned for {', '.join(gaps)}")
    if args.notify:
        notify(gaps)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
