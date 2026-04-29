#!/usr/bin/env python3
"""
Post-merge content-drift check on the live deployed site.

Run AFTER a publish PR merges + the deploy.yml run completes. Fetches
the live post HTML and asserts:

  - The page is reachable (HTTP 200).
  - No `id="TODO..."` GodboltEmbed placeholders survived the merge.
    (Caught the post-2 'wire-in lost between branches' failure.)
  - The page's heading + summary match the local mdx frontmatter
    (catches stale CDN / wrong commit / wrong post deployed).
  - The expected godbolt link appears (matches the YAML).
  - The expected `discussion:` URL (if frontmatter has one) is in the
    page body.

Usage:
    scripts/check-live-content.py --slug first-reflection
    scripts/check-live-content.py --slug splicing --base-url https://wrocpp.github.io

Exits non-zero on any drift; prints a punch-list of what's wrong.
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: PyYAML not installed")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE = "https://wrocpp.github.io"


def fetch(url: str, timeout: int = 15) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={
        "User-Agent": "wrocpp-drift-check/1.0",
        "Accept": "text/html,*/*",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def post_frontmatter(slug: str) -> dict:
    posts = sorted((REPO_ROOT / "src/content/posts").glob(f"*-{slug}.mdx"))
    if not posts:
        sys.exit(f"error: no mdx for slug {slug!r}")
    text = posts[0].read_text()
    end = text.find("\n---", 3)
    return yaml.safe_load(text[3:end]) or {}


def godbolt_ids_for(slug: str) -> list[str]:
    yml = REPO_ROOT / "src/data/godbolt-permalinks.yml"
    if not yml.exists():
        return []
    data = yaml.safe_load(yml.read_text()) or {}
    entries = data.get(slug, {}) or {}
    return [v.get("id") for v in entries.values() if isinstance(v, dict) and v.get("id")]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slug", required=True)
    p.add_argument("--base-url", default=DEFAULT_BASE)
    args = p.parse_args()

    fm = post_frontmatter(args.slug)
    url = f"{args.base_url}/posts/{args.slug}/"
    print(f"--> fetching {url}", file=sys.stderr)
    status, html = fetch(url)
    fails: list[str] = []

    if status != 200:
        fails.append(f"HTTP {status} (expected 200) -- post not live yet, or pubDate gating, or deploy stale")
        print(f"\nFAIL: {fails[0]}")
        return 2

    # 1. No TODO placeholders survived.
    todos = re.findall(r'id="(TODO[^"]*)"', html)
    if todos:
        fails.append(f"GodboltEmbed placeholder ids on live page: {todos}")

    # Also catch the rendered placeholder card (for the Astro-rendered case
    # where the id starts with TODO and the component renders the gray
    # "Click-to-run coming soon" card).
    if "PERMALINK PENDING" in html or "Click-to-run coming soon" in html:
        fails.append("rendered 'PERMALINK PENDING' / 'Click-to-run coming soon' card on live page")

    # 2. Title + summary match.
    title = fm.get("title", "")
    if title and title not in html:
        fails.append(f"frontmatter title {title!r} not found in live HTML")
    summary = fm.get("summary", "")
    if summary and summary[:60] not in html:
        fails.append(f"frontmatter summary not found in live HTML (first 60 chars: {summary[:60]!r})")

    # 3. Godbolt ids appear (at least one).
    ids = godbolt_ids_for(args.slug)
    if ids:
        present = [i for i in ids if f"godbolt.org/z/{i}" in html]
        missing = [i for i in ids if i not in present]
        if not present:
            fails.append(f"no godbolt id from YAML appears on the page (expected one of: {ids})")
        elif missing:
            print(f"note: not all variants linked from page (ok if not every variant has a GodboltEmbed): missing {missing}",
                  file=sys.stderr)

    # 4. Discussion URL (if frontmatter has one).
    discussion = fm.get("discussion")
    if discussion and discussion not in html:
        fails.append(f"frontmatter discussion: {discussion} not linked from live page")

    if fails:
        print("\nFAIL:")
        for f in fails:
            print(f"  - {f}")
        return 1

    print("ok   live post matches local frontmatter + YAML")
    return 0


if __name__ == "__main__":
    sys.exit(main())
