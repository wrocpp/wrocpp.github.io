#!/usr/bin/env python3
"""Check post titles against safe limits for social card rendering.

Social cards render titles in Quicksand 700 at 92pt on a 980px-wide
content area. Titles beyond ~65 characters wrap to 3+ lines and risk
colliding with the logo watermark or overflowing the card.

Usage:
  python3 scripts/check-social-title.py           # check all posts + social cards
  python3 scripts/check-social-title.py --file F   # check a single .mdx file

Exit code: 0 = all OK, 1 = at least one ERROR found.
"""

import argparse
import glob
import re
import sys
from pathlib import Path

FRONTMATTER_WARN = 90
FRONTMATTER_ERROR = 120
SOCIAL_H1_WARN = 65
SOCIAL_H1_ERROR = 90

YELLOW = "\033[33m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def extract_title_from_mdx(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*["\'](.+?)["\']', text, re.MULTILINE)
    if m:
        return m.group(1)
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip().strip("\"'")
    return None


def extract_h1_from_content_md(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# "):
            clean = re.sub(r"\{\.title-[a-z]+\}", "", line[2:]).strip()
            clean = re.sub(r'<span class="[^"]*">', "", clean)
            clean = clean.replace("</span>", "")
            return clean
    return None


def check_frontmatter(paths: list[Path]) -> list[str]:
    issues = []
    for p in sorted(paths):
        title = extract_title_from_mdx(p)
        if title is None:
            continue
        n = len(title)
        slug = p.stem.split("-", 3)[-1] if "-" in p.stem else p.stem
        if n > FRONTMATTER_ERROR:
            issues.append(f"{RED}ERROR{RESET}  {slug}: title is {n} chars (limit {FRONTMATTER_ERROR}): {title[:80]}...")
        elif n > FRONTMATTER_WARN:
            issues.append(f"{YELLOW}WARN{RESET}   {slug}: title is {n} chars (> {FRONTMATTER_WARN}): {title[:80]}...")
    return issues


def check_social_cards(root: Path) -> list[str]:
    issues = []
    for content_md in sorted(root.glob("social/*/*/content.md")):
        h1 = extract_h1_from_content_md(content_md)
        if h1 is None:
            continue
        n = len(h1)
        parts = content_md.parts
        slug = parts[-2] if len(parts) >= 2 else str(content_md)
        platform = parts[-3] if len(parts) >= 3 else "?"
        label = f"{platform}/{slug}"
        if n > SOCIAL_H1_ERROR:
            issues.append(f"{RED}ERROR{RESET}  {label}: h1 is {n} chars (limit {SOCIAL_H1_ERROR}): {h1[:80]}...")
        elif n > SOCIAL_H1_WARN:
            issues.append(f"{YELLOW}WARN{RESET}   {label}: h1 is {n} chars (> {SOCIAL_H1_WARN}): {h1[:80]}...")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, help="Check a single .mdx file")
    args = parser.parse_args()

    root = Path(".")
    has_error = False

    if args.file:
        if not args.file.exists():
            return
        if not args.file.suffix == ".mdx":
            return
        issues = check_frontmatter([args.file])
        for i in issues:
            print(i)
            if "ERROR" in i:
                has_error = True
        sys.exit(1 if has_error else 0)

    posts = list(root.glob("src/content/posts/*.mdx"))
    toolset = list(root.glob("src/content/toolset/*.mdx"))
    all_mdx = posts + toolset

    print(f"Checking {len(all_mdx)} frontmatter titles...")
    fm_issues = check_frontmatter(all_mdx)

    print(f"Checking social card h1 lines...")
    sc_issues = check_social_cards(root)

    all_issues = fm_issues + sc_issues

    if not all_issues:
        print(f"{GREEN}OK{RESET}  All titles within safe limits.")
        sys.exit(0)

    print()
    for i in all_issues:
        print(i)
        if "ERROR" in i:
            has_error = True

    print()
    print(f"Social card title guide:")
    print(f"  <= 65 chars: default 92pt (no class needed)")
    print(f"  66-90 chars: use .title-long (72pt)")
    print(f"  91-110 chars: use .title-xlong (56pt)")
    print(f"  > 110 chars: rewrite shorter")

    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
