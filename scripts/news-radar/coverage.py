#!/usr/bin/env python3
"""Which published posts already cover a topic, and does a post with this slug exist.

The radar uses it to separate news we already carry from gaps. Patterns are Python
(extended) regular expressions: alternation is a bare "|", never "\\|".

Usage:
    coverage.py                          # table of the built-in topics
    coverage.py --grep 'P2287|P3533'     # posts whose text matches
    coverage.py --expect-slug a --expect-slug b   # exit 1 unless each is a published post
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
POSTS_DIR = REPO / "src" / "content" / "posts"

# Topic name -> pattern. Extend as the radar finds new beats.
TOPICS: dict[str, str] = {
    "C++29 mode (-std=c++29 / c++2d)": r"std=c\+\+29|std=c\+\+2d",
    "GCC 17": r"GCC 17|gcc-17",
    "LLVM 23": r"LLVM 23|llvm-23|clang 23",
    "Brno meeting": r"Brno",
    "Búzios meeting": r"B[uú]zios",
    "WG21 mailing": r"WG21 .*mailing|pre-B[uú]zios",
    "DIS ballot": r"DIS ballot|Draft International Standard",
    "contracts": r"contracts?\b",
    "profiles": r"\bprofiles?\b",
    "std::execution": r"std::execution|senders",
    "std::hive": r"std::hive",
    "std::simd": r"std::simd|portable-simd",
    "Boost 1.92": r"Boost 1\.92",
    "Qt 6.12": r"Qt 6\.12",
    "MSVC 14.5x / VS 2026": r"MSVC 14\.5|Visual Studio 2026",
    "CMake / vcpkg / Conan": r"CMake|vcpkg|Conan",
    "P2287 base-class designators": r"P2287",
    "P3533 constexpr virtual inheritance": r"P3533|virtual inheritance",
    "CRA": r"\bCRA\b|Cyber Resilience",
    "Meeting C++ 2026": r"Meeting C\+\+ 2026",
}

_FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


@dataclass(frozen=True)
class Post:
    path: Path
    slug: str
    pub_date: str
    published: bool
    text: str


def _field(front: str, name: str) -> str:
    m = re.search(rf"^{name}:\s*\"?([^\"\n]+)\"?\s*$", front, re.M)
    return m.group(1).strip() if m else ""


def load_posts(posts_dir: Path = POSTS_DIR) -> list[Post]:
    posts = []
    for path in sorted(Path(posts_dir).glob("*.mdx")):
        text = path.read_text(encoding="utf-8")
        m = _FRONT.match(text)
        front = m.group(1) if m else ""
        slug = _field(front, "slug") or path.stem[11:]
        posts.append(
            Post(path=path, slug=slug, pub_date=_field(front, "pubDate"),
                 published=_field(front, "draft") != "true", text=text)
        )
    return posts


def matching(posts: list[Post], pattern: str) -> list[Post]:
    rx = re.compile(pattern)
    return [p for p in posts if p.published and rx.search(p.text)]


def topic_table(posts: list[Post], topics: dict[str, str] = TOPICS) -> list[tuple[str, list[Post]]]:
    return [(name, matching(posts, pat)) for name, pat in topics.items()]


def missing_slugs(posts: list[Post], slugs: list[str]) -> list[str]:
    have = {p.slug for p in posts if p.published}
    return [s for s in slugs if s not in have]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grep", help="extended regex to search published posts for")
    ap.add_argument("--expect-slug", action="append", default=[], help="slug that must be a published post")
    args = ap.parse_args()
    posts = load_posts()

    if args.expect_slug:
        missing = missing_slugs(posts, args.expect_slug)
        for s in args.expect_slug:
            print(("MISSING " if s in missing else "ok      ") + s)
        return 1 if missing else 0

    if args.grep:
        for p in matching(posts, args.grep):
            print(f"{p.pub_date}  {p.slug}")
        return 0

    for name, hits in topic_table(posts):
        latest = max(hits, key=lambda p: p.pub_date) if hits else None
        tail = f"latest {latest.pub_date} {latest.slug}" if latest else "NOT COVERED"
        print(f"{name}: {len(hits)} posts | {tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
