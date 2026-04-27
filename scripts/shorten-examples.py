#!/usr/bin/env python3
"""
Generate Compiler Explorer permalinks for a post's example sources.

For every `posts/<NN>-<slug>/examples/*.cpp` in the cpp26 examples repo,
POST the source to https://godbolt.org/api/shortener with the pinned
Bloomberg clang-p2996 compiler id and the series flags, then merge the
returned shortlink into src/data/godbolt-permalinks.yml.

Idempotent: skips variants that already have an `id` set, unless --force.

Usage:
    scripts/shorten-examples.py --post 02-first-reflection
    scripts/shorten-examples.py --post 02-first-reflection --force
    scripts/shorten-examples.py --post 02-first-reflection --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: PyYAML not installed. run: pip3 install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
YAML_PATH = REPO_ROOT / "src" / "data" / "godbolt-permalinks.yml"
CPP26_ROOT = Path("/Users/filipsajdak/dev/c++26")
COMPILER_ID = "clang_bb_p2996"
COMPILER_OPTIONS = "-std=c++26 -freflection-latest -stdlib=libc++"
SHORTENER_URL = "https://godbolt.org/api/shortener"


def slug_from_post(post_arg: str) -> tuple[str, str]:
    """Resolve `02-first-reflection` -> (NN-slug folder, mdx slug).

    The mdx slug is whatever the matching post's frontmatter `slug:` field
    says -- NOT just the folder name minus the NN- prefix. Post 1's folder
    is `01-why-it-matters` but its mdx slug is `why-cpp26-reflection-matters`,
    so a naive split would write the wrong YAML key.
    """
    parts = post_arg.split("-", 1)
    if len(parts) != 2 or not parts[0].isdigit():
        sys.exit(f"error: --post expects NN-slug form, got {post_arg!r}")
    nn = int(parts[0])

    # Find the mdx post whose series_order matches NN.
    posts_dir = REPO_ROOT / "src" / "content" / "posts"
    for mdx in sorted(posts_dir.glob("*.mdx")):
        text = mdx.read_text()
        if not text.startswith("---"):
            continue
        # Frontmatter: read until the closing ---
        end = text.find("\n---", 3)
        if end < 0:
            continue
        fm = yaml.safe_load(text[3:end])
        if fm and fm.get("series_order") == nn and fm.get("series") == "cpp26-reflection":
            return post_arg, fm["slug"]
    sys.exit(f"error: no mdx post with series_order={nn} found in {posts_dir}")


def shorten(source: str, title: str) -> dict:
    """Hit godbolt's shortener with one source file. Returns the parsed
    {id, url, title} we want to write into the YAML."""
    payload = {
        "sessions": [
            {
                "id": 1,
                "language": "c++",
                "source": source,
                "compilers": [
                    {"id": COMPILER_ID, "options": COMPILER_OPTIONS}
                ],
            }
        ]
    }
    req = urllib.request.Request(
        SHORTENER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    url = body.get("url")
    if not url:
        sys.exit(f"error: shortener returned no url: {body}")
    short_id = url.rsplit("/", 1)[-1]
    return {"id": short_id, "url": url, "title": title}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--post", required=True, help="post folder (e.g. 02-first-reflection)")
    p.add_argument("--force", action="store_true", help="overwrite existing entries")
    p.add_argument("--dry-run", action="store_true", help="print what would change")
    args = p.parse_args()

    nn_slug, slug = slug_from_post(args.post)
    examples_dir = CPP26_ROOT / "posts" / nn_slug / "examples"
    if not examples_dir.is_dir():
        sys.exit(f"error: not a directory: {examples_dir}")

    sources = sorted(p for p in examples_dir.glob("*.cpp"))
    if not sources:
        sys.exit(f"error: no .cpp files in {examples_dir}")

    yaml_data = {}
    if YAML_PATH.exists():
        with YAML_PATH.open() as f:
            yaml_data = yaml.safe_load(f) or {}
    yaml_data.setdefault(slug, {})

    changed = False
    for src in sources:
        variant = src.stem  # e.g. "teaser_peel"
        existing = yaml_data[slug].get(variant) or {}
        if existing.get("id") and not args.force:
            print(f"skip  {slug}.{variant}  (id={existing['id']})")
            continue
        title = existing.get("title") or variant.replace("_", " ").capitalize()
        source_text = src.read_text()
        if args.dry_run:
            print(f"DRY   {slug}.{variant}  ({src.name}, {len(source_text)} chars)")
            continue
        result = shorten(source_text, title)
        yaml_data[slug][variant] = result
        print(f"OK    {slug}.{variant}  -> {result['url']}")
        changed = True

    if changed and not args.dry_run:
        # Preserve the file header by re-reading and only rewriting from the
        # first non-comment line.
        header = []
        if YAML_PATH.exists():
            for line in YAML_PATH.read_text().splitlines(keepends=True):
                if line.startswith("#") or line.strip() == "":
                    header.append(line)
                else:
                    break
        body = yaml.safe_dump(yaml_data, sort_keys=False, allow_unicode=False, width=120)
        YAML_PATH.write_text("".join(header) + body)
        print(f"\nwrote {YAML_PATH.relative_to(REPO_ROOT)}")
    elif args.dry_run:
        print("\n(dry-run; YAML not written)")
    else:
        print("\nnothing to do (all variants already have ids)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
