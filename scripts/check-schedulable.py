#!/usr/bin/env python3
"""Report future posts the Buffer auto-scheduler would silently skip.

auto-schedule-next.py only queues a post it considers "prepared": OG image,
both card images, and a caption.md for each platform. A post missing any of
those is passed over with no warning, so the site publishes on schedule and
nothing goes out on social. Nobody notices until someone reads the queue.

That happened on 2026-08-19 and 2026-08-20: both posts went live, neither had
a caption, and neither reached LinkedIn or Facebook. The cause was a
card-building script that wrote content.md and config.yaml and stopped there.

This mirrors is_prepared() from the scheduler. Keep them in step.

Usage:
  scripts/check-schedulable.py            # future posts only
  scripts/check-schedulable.py --strict   # exit 1 if any are unschedulable
"""
import argparse
import datetime as dt
import glob
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

REQUIRED = [
    "public/og/{slug}.png",
    "social/linkedin/{slug}/image.png",
    "social/linkedin/{slug}/caption.md",
    "social/facebook/{slug}/image.png",
    "social/facebook/{slug}/caption.md",
]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--today", default=None)
    args = ap.parse_args()
    today = args.today or dt.date.today().isoformat()

    bad = []
    total = 0
    for path in sorted(glob.glob(str(REPO / "src/content/posts/*.mdx"))):
        text = Path(path).read_text(encoding="utf-8")
        d = re.search(r"^pubDate:\s*(\S+)", text, re.M)
        s = re.search(r'^slug:\s*"?([A-Za-z0-9-]+)', text, re.M)
        draft = re.search(r"^draft:\s*(\S+)", text, re.M)
        if not (d and s):
            continue
        if draft and draft.group(1).strip().lower() == "true":
            continue
        date = d.group(1).strip().strip('"')
        if date < today:
            continue
        total += 1
        slug = s.group(1)
        missing = [p.format(slug=slug) for p in REQUIRED
                   if not (REPO / p.format(slug=slug)).exists()]
        if missing:
            bad.append((date, slug, missing))

    for date, slug, missing in bad:
        print(f"\n{date}  {slug}")
        for m in missing:
            print(f"    missing  {m}")

    print()
    if bad:
        print(f"{len(bad)} of {total} future posts would be SKIPPED by the scheduler.")
        print("Each one publishes on the site and never reaches social.")
    else:
        print(f"OK: all {total} future posts are schedulable.")
    return 1 if (bad and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
