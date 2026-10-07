#!/usr/bin/env python3
"""Check that a prose rewrite of a post changed wording only.

Compares the post at a base ref (git show) with the working copy and fails (exit 1) when
any of these differ or vanished: fenced code blocks, number tokens, URLs, MDX components
with their props, heading text, and every frontmatter field except `summary` and
`updatedDate`. Headings may be ADDED (a split section, "In short"); none may disappear.
Prints a before/after table of readability metrics.

Usage:
  scripts/check-rewrite-invariants.py origin/main --slug S
  scripts/check-rewrite-invariants.py origin/main --file src/content/posts/X.mdx
  scripts/check-rewrite-invariants.py - --file NEW.mdx --base-file OLD.mdx   # no git (tests)

Exit code: 0 = invariants hold, 1 = violation, 2 = usage / not found. ASCII output.
"""

import argparse
import importlib.util
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXEMPT_FIELDS = {"summary", "updatedDate"}
URL_RE = re.compile(r"https?://[^\s)<>\"'\]]+")
LINK_TARGET_RE = re.compile(r"\]\(([^)\s]+)")
TAG_RE = re.compile(r"<([A-Z][A-Za-z0-9]*)\b([^<>]*?)/?>", re.DOTALL)
NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
SPAN_RE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
METRIC_ROWS = [("prose words", "words"), ("mean sentence", "mean_sent"), ("sentences over 25 (count)", "n_over25"),
               ("Fog", "fog"), ("spans per 100 words", "spans_per100"), ("sentences with 3+ spans %", "sent3_share"),
               ("headings", "headings"), ("max section words", "max_section_words"),
               ("longest prose run", "max_prose_run"), ("list items", "list_items"), ("In short", "in_short")]


def load_report():
    spec = importlib.util.spec_from_file_location("readability_report", Path(__file__).resolve().parent / "readability-report.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def split_parts(text):
    """(frontmatter fields, fenced code blocks, body text outside fences)."""
    report = load_report()
    fm, body, _ = report.split_frontmatter(text)
    fields = report.frontmatter_fields(fm)
    blocks, prose, cur, fence = [], [], None, ""
    for line in body:
        m = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            cur.append(line)
            if m and m.group(1)[0] == fence:
                blocks.append("\n".join(cur))
                fence = ""
        elif m:
            fence, cur = m.group(1)[0], [line]
        else:
            prose.append(line)
    return fields, blocks, "\n".join(prose)


def headings_of(prose):
    return [re.sub(r"\s+", " ", m.group(2)).strip() for m in re.finditer(r"^(#{1,6})\s+(.*?)\s*$", prose, re.MULTILINE)]


def components_of(prose):
    no_spans = SPAN_RE.sub(" ", prose)
    return Counter(f"{n} {' '.join(p.split())}" for n, p in TAG_RE.findall(no_spans))


def urls_of(prose):
    return set(URL_RE.findall(prose)) | set(LINK_TARGET_RE.findall(prose))


def numbers_of(prose):
    t = re.sub(r"^\s*(#{1,6}\s+)?(\d+[.)])\s+", "", prose, flags=re.MULTILINE)
    t = TAG_RE.sub(" ", t)
    t = URL_RE.sub(" ", LINK_TARGET_RE.sub("](", t))
    return {n.rstrip(".,") for n in NUMBER_RE.findall(t)}


def diff_sets(label, before, after, out):
    for item in sorted(before - after):
        out.append(f"{label} vanished or changed: {item[:100]!r}")
    for item in sorted(after - before):
        out.append(f"{label} new or changed: {item[:100]!r}")


def diff_fields(before, after, out):
    for key in sorted((set(before) | set(after)) - EXEMPT_FIELDS):
        if before.get(key) != after.get(key):
            out.append(f"frontmatter {key} changed: {before.get(key)!r} -> {after.get(key)!r}"[:200])


def check(base_text, new_text):
    """List of violation messages (empty when every invariant holds)."""
    bf, bc, bp = split_parts(base_text)
    nf, nc, np_ = split_parts(new_text)
    out = []
    diff_fields(bf, nf, out)
    if bc != nc:
        out.append(f"fenced code blocks differ: {len(bc)} before, {len(nc)} after"
                   + "".join(f"; block {i + 1} changed" for i, (a, b) in enumerate(zip(bc, nc)) if a != b))
    diff_sets("number", numbers_of(bp), numbers_of(np_), out)
    diff_sets("url", urls_of(bp), urls_of(np_), out)
    comp_b, comp_n = components_of(bp), components_of(np_)
    diff_sets("component", set(comp_b), set(comp_n), out)
    for tag in comp_b:
        if tag in comp_n and comp_b[tag] != comp_n[tag]:
            out.append(f"component count changed for {tag[:80]!r}: {comp_b[tag]} -> {comp_n[tag]}")
    gone = Counter(headings_of(bp)) - Counter(headings_of(np_))
    out.extend(f"heading vanished or changed: {h!r}" for h in sorted(gone))
    return out


def metric_table(base_text, new_text):
    report = load_report()
    before, after = report.analyze(base_text)[0], report.analyze(new_text)[0]
    lines = [f"{'metric':32} {'before':>9} {'after':>9}"]
    lines += [f"{label:32} {before[k]!s:>9} {after[k]!s:>9}" for label, k in METRIC_ROWS]
    return "\n".join(lines)


def git_show(ref, path):
    rel = Path(path).resolve().relative_to(ROOT)
    r = subprocess.run(["git", "show", f"{ref}:{rel.as_posix()}"], capture_output=True, text=True, cwd=ROOT)
    return r.stdout if r.returncode == 0 else None


def resolve_target(args):
    if args.file:
        return args.file
    hits = sorted((ROOT / "src/content/posts").glob(f"*-{args.slug}.mdx")) if args.slug else []
    return hits[0] if hits else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base_ref", help="git ref to compare against, e.g. origin/main ('-' with --base-file)")
    ap.add_argument("--slug")
    ap.add_argument("--file", type=Path)
    ap.add_argument("--base-file", type=Path, help="read the base text from a file instead of git")
    args = ap.parse_args()
    target = resolve_target(args)
    if target is None or not Path(target).exists():
        print("ERROR: post not found (use --slug or --file)")
        return 2
    base = Path(args.base_file).read_text(encoding="utf-8") if args.base_file else git_show(args.base_ref, target)
    if base is None:
        print(f"ERROR: {target} does not exist at {args.base_ref}")
        return 2
    new = Path(target).read_text(encoding="utf-8")
    print(metric_table(base, new))
    problems = check(base, new)
    for p in problems:
        print(f"FAIL {p}")
    print("invariants: " + (f"{len(problems)} violation(s)" if problems else "hold"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
