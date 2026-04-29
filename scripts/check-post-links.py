#!/usr/bin/env python3
"""
Link-resolution sweep on the production-built dist for one post.

Run AFTER `npm run build`; greps the post's HTML for every `href` and
verifies:

  - relative URLs (no scheme) -> the path exists in dist/
  - https://wrocpp.github.io/... -> the path exists in dist/ (same site)
  - external https?://... -> HEAD-fetched, must return 2xx/3xx (not 404)

Catches the failure mode where a forward reference to /posts/<slug>/
slipped past PostLink (which would gate it to plain text until that
post's pubDate). Without this check, the post-2 fire-drill scenario
plays out for every post: live page, broken internal link.

Usage:
    scripts/check-post-links.py --slug why-cpp26-reflection-matters
    scripts/check-post-links.py --slug splicing --no-external

Exits non-zero if any link fails to resolve.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST = REPO_ROOT / "dist"
SITE_HOST = "wrocpp.github.io"


def post_html(slug: str) -> Path:
    p = DIST / "posts" / slug / "index.html"
    if not p.exists():
        sys.exit(f"error: {p} not in dist -- did `npm run build` run? "
                 f"Or post is gated by isPublished (pubDate in future).")
    return p


def hrefs(html: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', html)


def head_ok(url: str, timeout: float = 8) -> tuple[bool, int | str]:
    """HEAD-fetch a URL. Some servers reject HEAD; fall back to GET range
    bytes 0-0 if HEAD returns 4xx/5xx."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": "wrocpp-link-check/1.0",
                "Accept": "*/*",
            })
            if method == "GET":
                req.add_header("Range", "bytes=0-0")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status < 400, resp.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (405, 403):
                continue
            return False, e.code
        except (urllib.error.URLError, TimeoutError) as e:
            return False, str(e)[:120]
    return False, "all-methods-failed"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slug", required=True)
    p.add_argument("--no-external", action="store_true",
                   help="skip http(s) URLs to other domains (fastest mode)")
    args = p.parse_args()

    html = post_html(args.slug).read_text()
    seen_internal: set[str] = set()
    seen_external: set[str] = set()
    fails: list[tuple[str, str]] = []

    for href in hrefs(html):
        if href.startswith("#") or href.startswith("mailto:") or href.startswith("tel:"):
            continue
        if href.startswith("/") or href.startswith(f"https://{SITE_HOST}"):
            # Treat as internal: strip host + query/fragment, look in dist.
            path = href.replace(f"https://{SITE_HOST}", "")
            path = path.split("?", 1)[0].split("#", 1)[0]
            if path in seen_internal:
                continue
            seen_internal.add(path)
            target = DIST / path.lstrip("/")
            # Astro emits /<dir>/index.html for trailing-slash routes; map.
            candidates = [target, target / "index.html"]
            if not any(c.exists() for c in candidates):
                fails.append((href, f"missing in dist: {target.relative_to(DIST)}"))
                continue
            print(f"ok   internal {href}")
            continue

        if not href.startswith(("http://", "https://")):
            continue  # skip exotic schemes

        if args.no_external:
            continue
        if href in seen_external:
            continue
        seen_external.add(href)
        ok, status = head_ok(href)
        marker = "ok  " if ok else "FAIL"
        print(f"{marker} external {href}  [{status}]")
        if not ok:
            fails.append((href, f"http {status}"))

    print()
    print(f"checked: {len(seen_internal)} internal, {len(seen_external)} external")
    if fails:
        print(f"\n{len(fails)} failure(s):")
        for url, why in fails:
            print(f"  - {url}\n      {why}")
        return 1
    print("all links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
