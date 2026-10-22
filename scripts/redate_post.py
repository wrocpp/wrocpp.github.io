#!/usr/bin/env python3
"""Move one post to another day: the post file and its pubDate, and the dates of its LinkedIn and Facebook cards.

  scripts/redate_post.py --slug SLUG --to YYYY-MM-DD [--dry-run] [--no-render] [--root DIR]

What changes (and nothing else):
  src/content/posts/<old>-<slug>.mdx   renamed with `git mv`, `pubDate:` set to the new day
  social/<platform>/<slug>/config.yaml, content.md, index.html   the card date, when it is the old day
  social/<platform>/<slug>/caption.md  the "Suggested post time" line, only when it names the old day
  social/<platform>/<slug>/image.png   re-rendered with `brand-gen image`
  public/og/<slug>.png                 a copy of the LinkedIn image

A card, config or index file that carries a date other than the old day is reported and left alone: nothing in it
says what the other date means. Caption lines that name some other day are left alone too.

The Buffer queue is not touched here: a post that is already queued has to be deleted and created again (see
docs of push-to-buffer.py), and scripts/check-pubdates.py must pass afterwards.
"""
import argparse
import datetime
import re
import shutil
import subprocess
import sys
from pathlib import Path

PLATFORMS = ("linkedin", "facebook")
ISO = re.compile(r"\b(20\d\d-\d\d-\d\d)\b")
PUBDATE = re.compile(r"^pubDate:\s*(\d{4}-\d{2}-\d{2})\s*$", re.M)
TIME_LINE = re.compile(r"^(?P<day>[A-Z][a-z]+) (?P<date>\d{4}-\d{2}-\d{2})(?P<rest>,.*)$")


def weekday(day):
    return datetime.date.fromisoformat(day).strftime("%A")


def post_file(root, slug):
    found = sorted((root / "src/content/posts").glob(f"20??-??-??-{slug}.mdx"))
    if len(found) != 1:
        raise SystemExit(f"expected one post file for {slug}, found {[f.name for f in found]}")
    return found[0]


def retime_caption(text, old, new):
    """The 'Suggested post time' line, when it names the old day: new weekday and day, same time and zone."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.strip() != "## Suggested post time" or i + 1 >= len(lines):
            continue
        match = TIME_LINE.match(lines[i + 1])
        if match and match["date"] == old:
            lines[i + 1] = f"{weekday(new)} {new}{match['rest']}"
    return "\n".join(lines)


def redate_card_file(path, old, new, notes):
    text = path.read_text()
    dates = set(ISO.findall(text))
    if old not in dates:
        notes.append(f"{path}: no {old} in it")
        return None
    if dates - {old}:
        notes.append(f"{path}: also names {sorted(dates - {old})}, left alone")
        return None
    return text.replace(old, new)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--to", required=True, dest="new", help="the new day, YYYY-MM-DD")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args(argv)
    root, slug, new = Path(args.root), args.slug, args.new
    datetime.date.fromisoformat(new)

    source = post_file(root, slug)
    old = source.name[:10]
    body = source.read_text()
    match = PUBDATE.search(body)
    if not match or match[1] != old:
        raise SystemExit(f"{source.name}: pubDate {match[1] if match else None} does not match the file name")
    if old == new:
        raise SystemExit("the post is already on that day")
    target = source.with_name(f"{new}-{slug}.mdx")
    if target.exists():
        raise SystemExit(f"{target.name} exists")

    notes, edits = [], {}
    edits[source] = PUBDATE.sub(f"pubDate: {new}", body, count=1)
    for platform in PLATFORMS:
        card = root / "social" / platform / slug
        if not card.is_dir():
            notes.append(f"no card directory {card}")
            continue
        for name in ("config.yaml", "content.md", "index.html"):
            if (card / name).exists():
                changed = redate_card_file(card / name, old, new, notes)
                if changed is not None:
                    edits[card / name] = changed
        caption = card / "caption.md"
        if caption.exists():
            retimed = retime_caption(caption.read_text(), old, new)
            if retimed != caption.read_text():
                edits[caption] = retimed

    print(f"{slug}: {old} -> {new}: {len(edits)} files")
    for note in notes:
        print(f"  note: {note}")
    if args.dry_run:
        for path in edits:
            print(f"  would edit {path.relative_to(root)}")
        return 0

    subprocess.run(["git", "mv", str(source), str(target)], cwd=root, check=True)
    for path, text in edits.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        (target if path == source else path).write_text(text)

    if not args.no_render:
        for platform in PLATFORMS:
            card = root / "social" / platform / slug
            if not (card / "index.html").exists():
                continue
            subprocess.run(["brand-gen", "image"], cwd=card, check=True, capture_output=True)
            rendered = card / f"{slug}.png"
            if not rendered.exists():
                raise SystemExit(f"brand-gen wrote no {rendered}")
            shutil.move(rendered, card / "image.png")
        shutil.copy(root / "social/linkedin" / slug / "image.png", root / "public/og" / f"{slug}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
