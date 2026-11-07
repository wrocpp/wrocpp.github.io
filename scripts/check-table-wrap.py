#!/usr/bin/env python3
"""Fail if a built page has a <table> that cannot scroll sideways on a phone.

body has overflow-x: clip, so a table wider than the viewport is cut off with no
way to reach its columns. Every <table> must sit directly inside a container that
decides how it fits: .table-wrap or .table-scroll (both scroll) or .table-fit
(fixed layout, fits by design). astro.config.mjs wraps Markdown tables in
.table-wrap; hand-written tables carry the class themselves.

Usage: scripts/check-table-wrap.py [DIR]    # DIR defaults to dist
Exit 0 when every table is contained, 1 otherwise (one line per offender).
"""

import sys
from html.parser import HTMLParser
from pathlib import Path

CONTAINERS = frozenset({"table-wrap", "table-scroll", "table-fit"})
VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
})
DEFAULT_DIR = "dist"


def class_names(attrs):
    return frozenset(dict(attrs).get("class", "").split())


class TableFinder(HTMLParser):
    """Collects (line, column) of every table whose parent is not a container."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.offenders = []

    def handle_starttag(self, tag, attrs):
        if tag == "table" and not self.parent_is_container():
            self.offenders.append(self.getpos())
        if tag not in VOID_TAGS:
            self.stack.append((tag, class_names(attrs)))

    def handle_startendtag(self, tag, attrs):
        if tag == "table" and not self.parent_is_container():
            self.offenders.append(self.getpos())

    def handle_endtag(self, tag):
        for depth in range(len(self.stack) - 1, -1, -1):
            if self.stack[depth][0] == tag:
                del self.stack[depth:]
                return

    def parent_is_container(self):
        return bool(self.stack) and bool(self.stack[-1][1] & CONTAINERS)


def uncontained_tables(html):
    finder = TableFinder()
    finder.feed(html)
    return finder.offenders


def check(root):
    problems = []
    for page in sorted(Path(root).rglob("*.html")):
        for line, column in uncontained_tables(page.read_text(encoding="utf-8", errors="replace")):
            problems.append(f"{page}:{line}:{column}: <table> is not inside .table-wrap, .table-scroll or .table-fit")
    return problems


def main(argv):
    root = argv[1] if len(argv) > 1 else DEFAULT_DIR
    if not Path(root).is_dir():
        print(f"error: {root} is not a directory (build the site first)", file=sys.stderr)
        return 2
    problems = check(root)
    for problem in problems:
        print(problem)
    print(f"check-table-wrap: {len(problems)} uncontained table(s) under {root}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
