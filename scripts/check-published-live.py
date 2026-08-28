#!/usr/bin/env python3
"""Verify that every post whose pubDate has arrived is actually reachable live.

The site is a static build, so a post exists on the internet only once a build
runs on or AFTER its pubDate. Buffer fires the social post on its own schedule
regardless of whether that build happened. When the build does not happen, the
social post points at a 404 and nothing notices.

That is not hypothetical. On 2026-08-27 GitHub dropped all three scheduled
deploy runs (03:30, 05:30 and 07:00 UTC; the workflow was active, unconditional
and unchanged, and a manual dispatch succeeded immediately). The day's post,
verification-asm-llvm-mca, stayed 404 for hours while its Facebook and LinkedIn
posts pointed at it. The first signal was a human clicking their own social post.

deploy.yml already runs three staggered crons, but that mitigation is aimed at
GitHub's scheduler running LATE. It does nothing when the runs are dropped
outright, because three times zero is zero.

Checks a trailing window rather than only today, so an outage lasting more than
a day is still caught on the following run.

Usage:
  scripts/check-published-live.py                  # last 3 days of published posts
  scripts/check-published-live.py --days 7
  scripts/check-published-live.py --json           # machine-readable, for CI

Exit code: 0 = every due post is live, 1 = at least one is missing.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = REPO / "src" / "content" / "posts"
DEFAULT_BASE_URL = "https://wrocpp.github.io"

PUBDATE_RE = re.compile(r"^pubDate:\s*(\S+)", re.MULTILINE)
SLUG_RE = re.compile(r'^slug:\s*"?([^"\n]+)"?', re.MULTILINE)
DRAFT_RE = re.compile(r"^draft:\s*(\S+)", re.MULTILINE)


def parse_posts() -> list[dict]:
    out = []
    for path in sorted(POSTS.glob("*.mdx")):
        text = path.read_text(encoding="utf-8")
        head = text.split("---", 2)[1] if text.startswith("---") else text[:2000]
        m_date = PUBDATE_RE.search(head)
        if not m_date:
            continue
        try:
            pub = dt.date.fromisoformat(m_date.group(1).strip().strip('"')[:10])
        except ValueError:
            continue
        m_slug = SLUG_RE.search(head)
        slug = m_slug.group(1).strip() if m_slug else path.stem
        m_draft = DRAFT_RE.search(head)
        draft = bool(m_draft) and m_draft.group(1).strip().lower() == "true"
        out.append({"slug": slug, "pubDate": pub, "draft": draft, "file": path.name})
    return out


def head_status(url: str, timeout: int = 20) -> int:
    """Return the HTTP status for url. GitHub Pages answers HEAD, but fall back
    to GET so a 405 from any future host does not read as an outage."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", "wrocpp-check-published-live/1")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status
        except urllib.error.HTTPError as e:
            if e.code == 405 and method == "HEAD":
                continue
            return e.code
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"     network error on {url}: {e}", file=sys.stderr)
            return 0
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL)
    ap.add_argument("--days", type=int, default=3,
                    help="how many days back to check (default 3)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = ap.parse_args()

    today = dt.datetime.now(dt.timezone.utc).date()
    earliest = today - dt.timedelta(days=args.days - 1)

    due = [p for p in parse_posts()
           if not p["draft"] and earliest <= p["pubDate"] <= today]

    results = []
    for p in sorted(due, key=lambda p: p["pubDate"]):
        url = f"{args.base_url.rstrip('/')}/posts/{p['slug']}/"
        status = head_status(url)
        results.append({
            "slug": p["slug"],
            "pubDate": p["pubDate"].isoformat(),
            "url": url,
            "status": status,
            "live": status == 200,
        })

    missing = [r for r in results if not r["live"]]

    if args.json:
        print(json.dumps({
            "checked": len(results),
            "missing": len(missing),
            "today": today.isoformat(),
            "results": results,
        }, indent=2))
    else:
        if not results:
            print(f"No published posts in the last {args.days} day(s) "
                  f"(window {earliest} .. {today}); nothing to check.")
        for r in results:
            mark = "ok  " if r["live"] else "FAIL"
            print(f"{mark} {r['pubDate']}  {r['slug']}  [{r['status']}]")
        print()
        if missing:
            print(f"FAIL: {len(missing)} published post(s) are not reachable.")
            print("The most likely cause is that no build has run since the pubDate")
            print("rolled over. Trigger one and re-check:")
            print("  gh workflow run 'Build & Deploy' --ref main")
        else:
            print(f"OK: all {len(results)} published post(s) in the last "
                  f"{args.days} day(s) are live.")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
