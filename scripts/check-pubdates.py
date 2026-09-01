#!/usr/bin/env python3
"""Guard the publishing schedule: one post per day, filenames that tell the truth.

Two distinct failure modes, learned the hard way:

1. DUPLICATE pubDate (ERROR). The site publishes on a daily cadence and Buffer
   fires exactly one 08:00Z social slot per channel per day. Two posts sharing a
   pubDate therefore means one of them goes out with no social post at all, and
   nothing in the build previously noticed. This has happened three times
   (2026-06-28, 2026-06-30, and 2026-08-20, the last caught by hand).

2. Filename date prefix disagreeing with pubDate (WARN). Re-dating a post
   without `git mv`-ing the file leaves a name that lies. Nothing breaks -- URLs
   are slug-based, not date-based -- but it makes the schedule unreadable at a
   glance and has already caused one wrong conclusion about which day was free.

Usage:
  scripts/check-pubdates.py            # check src/content/posts
  scripts/check-pubdates.py --strict   # also fail on WARN-level findings

Exit code: 0 = clean, 1 = at least one ERROR (or WARN under --strict).
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = REPO / "src" / "content" / "posts"

# Collisions that already published. They cannot be fixed now -- re-dating a
# post that is live rewrites history for no benefit -- so they are recorded here
# rather than failing every build. Do NOT add to this list to silence a NEW
# collision on a future date; move the post to a free day instead.
KNOWN_PAST_COLLISIONS = {
    "2026-06-28",  # reflect-tracing + hello-sender
    "2026-06-30",  # structured-concurrency + gor-nishanov-memorial
    # llvm-23-1-shipped + reflect-special-members. Different cause from the two
    # above, and the one worth reading before adding a third entry here.
    #
    # reflect-special-members was scheduled for 2026-09-01 and Buffer had
    # already queued its social posts. On 2026-08-29 it was re-dated to
    # 2026-10-28 to free the slot, and the Buffer queue was not reconciled.
    # Both social posts fired on schedule at 08:01Z on 2026-09-01, pointing at
    # a URL that would not exist until October, and a reader hit the 404.
    #
    # Sent posts cannot be recalled from LinkedIn or Facebook, so the only fix
    # that helps that reader is to make the advertised URL resolve. The post was
    # moved back to 2026-09-01, colliding with the post that had taken its slot.
    #
    # The usual reason a collision is an error does not apply: that rule exists
    # because one of the two posts would publish with no social post, and here
    # both had already been sent. Before re-dating anything inside the Buffer
    # window, run scripts/check-buffer-status.py --slug <slug> --kind post.
    "2026-09-01",
}

PUBDATE_RE = re.compile(r"^pubDate:\s*(\S+)", re.MULTILINE)
FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


def red(s: str) -> str:
    return f"\033[31m{s}\033[0m"


def green(s: str) -> str:
    return f"\033[32m{s}\033[0m"


def yellow(s: str) -> str:
    return f"\033[33m{s}\033[0m"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="treat WARN-level findings as failures too")
    args = parser.parse_args()

    if not POSTS.is_dir():
        print(f"{red('ERROR')} posts directory not found: {POSTS}")
        return 1

    by_date: dict[str, list[str]] = defaultdict(list)
    name_mismatches: list[tuple[str, str, str]] = []
    missing: list[str] = []

    for path in sorted(POSTS.glob("*.mdx")):
        text = path.read_text(encoding="utf-8")
        m = PUBDATE_RE.search(text)
        if not m:
            missing.append(path.name)
            continue
        pub = m.group(1).strip().strip('"').strip("'")
        by_date[pub].append(path.name)

        fm = FILENAME_DATE_RE.match(path.name)
        if fm and fm.group(1) != pub:
            name_mismatches.append((path.name, fm.group(1), pub))

    errors: list[str] = []
    warnings: list[str] = []

    for name in missing:
        errors.append(f"{red('ERROR')} {name}: no pubDate in frontmatter")

    for date, names in sorted(by_date.items()):
        if len(names) < 2:
            continue
        if date in KNOWN_PAST_COLLISIONS:
            warnings.append(
                f"{yellow('WARN')}  {date}: {len(names)} posts share this date "
                f"({', '.join(names)}); known past collision, already published"
            )
        else:
            errors.append(
                f"{red('ERROR')} {date}: {len(names)} posts share this date "
                f"({', '.join(names)}). The daily cadence allows one post per day "
                f"and Buffer fires one social slot per day, so one of these would "
                f"publish with no social post. Move one to a free date."
            )

    for name, filedate, pub in name_mismatches:
        warnings.append(
            f"{yellow('WARN')}  {name}: filename says {filedate} but pubDate is {pub}; "
            f"git mv the file so the name matches"
        )

    for w in warnings:
        print(w)
    for e in errors:
        print(e)

    total = len(by_date) and sum(len(v) for v in by_date.values())
    print()
    if errors:
        print(f"{red('FAIL')}: {len(errors)} error(s) across {total} posts.")
        return 1
    if warnings and args.strict:
        print(f"{red('FAIL')}: {len(warnings)} warning(s) under --strict.")
        return 1
    print(green(f"OK: {total} posts, no scheduling conflicts."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
