#!/usr/bin/env python3
"""
Stale-snapshot guard for the per-page llms.txt routes.

Each toolset entry under src/content/toolset/*.mdx that ships
`agentInstructions` in its frontmatter is rendered verbatim as
/toolset/<slug>/llms.txt. Nothing in the build couples that field to the
page body, so it is easy to rewrite the body and forget to refresh
agentInstructions -- the per-page llms.txt then describes a story the
page no longer tells.

This script enforces the coupling. For every entry with
`agentInstructions`, it computes the SHA256 of the body content
(everything after the closing frontmatter delimiter) and compares it
to the recorded `bodyHash` field. Any mismatch fails the build with a
hint that you need to re-review agentInstructions and update the
hash. Editing only the frontmatter (e.g. bumping `lastReviewed`) does
NOT trigger the check; only body edits do.

Idempotent. Runs in ~50ms across the toolset collection.

Usage:
    scripts/check-llms-sync.py                  # check; non-zero on drift
    scripts/check-llms-sync.py --update         # rewrite bodyHash in place
                                                # (use AFTER reviewing
                                                # agentInstructions)

Wired into npm prebuild so `npm run build` will not produce a stale
llms.txt.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLSET_DIR = REPO_ROOT / "src" / "content" / "toolset"


def split_frontmatter(text: str) -> tuple[str, str, str]:
    """Return (leading_delim_block, frontmatter_yaml, body).

    leading_delim_block includes the opening "---\n" and the closing
    "---\n" so re-assembly is trivial: leading + body == original (when
    we don't touch the frontmatter), or new_leading + body when we do.
    """
    if not text.startswith("---\n"):
        return "", "", text  # no frontmatter; treat the whole thing as body
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", "", text
    fm_yaml = text[4:end]
    leading = text[: end + len("\n---\n")]
    body = text[end + len("\n---\n") :]
    return leading, fm_yaml, body


def body_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_field(yaml: str, key: str) -> str | None:
    """Return the scalar value of a top-level key, or None if absent.

    We do not pull in PyYAML for this; a one-off scalar lookup is
    enough and avoids the dependency.
    """
    needle = f"{key}:"
    for line in yaml.splitlines():
        if line.startswith(needle):
            value = line[len(needle):].strip()
            # Strip surrounding quotes if present.
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]
            return value
    return None


def has_block_field(yaml: str, key: str) -> bool:
    """True if the key is present (any value, including a block scalar)."""
    needle = f"{key}:"
    return any(line.startswith(needle) for line in yaml.splitlines())


def upsert_body_hash(leading: str, fm_yaml: str, new_hash: str) -> str:
    """Return a replacement leading block with bodyHash set to new_hash.

    Inserts the field at the end of the frontmatter if absent. Otherwise
    rewrites the existing line in place.
    """
    lines = fm_yaml.splitlines()
    new_line = f"bodyHash: {new_hash}"
    for i, line in enumerate(lines):
        if line.startswith("bodyHash:"):
            lines[i] = new_line
            break
    else:
        lines.append(new_line)
    new_yaml = "\n".join(lines)
    return f"---\n{new_yaml}\n---\n"


def check_entry(path: Path, *, update: bool) -> bool:
    """Return True if the entry is in sync (or was just updated)."""
    text = path.read_text()
    leading, fm_yaml, body = split_frontmatter(text)
    if not has_block_field(fm_yaml, "agentInstructions"):
        return True  # no per-page llms.txt; nothing to keep in sync

    actual = body_sha256(body)
    recorded = extract_field(fm_yaml, "bodyHash")

    if recorded == actual:
        return True

    if update:
        new_leading = upsert_body_hash(leading, fm_yaml, actual)
        path.write_text(new_leading + body)
        action = "added" if recorded is None else "updated"
        print(f"  {path.name}: bodyHash {action} -> {actual[:16]}...")
        return True

    rel = path.relative_to(REPO_ROOT)
    if recorded is None:
        print(f"FAIL {rel}")
        print(f"     missing `bodyHash` in frontmatter; run with --update")
        print(f"     once you have reviewed agentInstructions against the body.")
        print(f"     bootstrap value: {actual}")
    else:
        print(f"FAIL {rel}")
        print(f"     body changed since bodyHash was recorded.")
        print(f"     recorded: {recorded}")
        print(f"     actual:   {actual}")
        print(f"     review agentInstructions for accuracy, then run:")
        print(f"     scripts/check-llms-sync.py --update")
    return False


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--update", action="store_true",
                   help="rewrite bodyHash in place (after reviewing "
                        "agentInstructions)")
    args = p.parse_args()

    entries = sorted(TOOLSET_DIR.glob("*.mdx"))
    if not entries:
        print(f"no toolset entries found in {TOOLSET_DIR}")
        return 0

    if args.update:
        print(f"Updating bodyHash across {len(entries)} toolset entr{'y' if len(entries)==1 else 'ies'}:")
    failures = 0
    for entry in entries:
        if not check_entry(entry, update=args.update):
            failures += 1

    if failures:
        print()
        print(f"{failures} entr{'y' if failures==1 else 'ies'} drifted; build refuses to proceed.")
        print("Per-page llms.txt may misrepresent the page body.")
        return 1
    if not args.update:
        print(f"OK -- {len(entries)} toolset entr{'y' if len(entries)==1 else 'ies'} in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
