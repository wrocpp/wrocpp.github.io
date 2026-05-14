#!/usr/bin/env python3
"""
Post a launch announcement to wro.cpp Slack #general via Incoming Webhook.

Reads the webhook URL from ~/.claude/secrets/wrocpp-slack-webhook (chmod 600).
The URL is NEVER printed to stdout/stderr -- only the resulting Slack message text.

Usage:
    scripts/push-to-slack.py --slug memory-safety-cpp26-and-beyond --kind toolset
    scripts/push-to-slack.py --slug enum-to-string --kind post
    scripts/push-to-slack.py --slug enum-to-string --kind post --dry-run

The message format pulls (title, summary) from the matching mdx frontmatter
and links to the live wro.cpp URL. The kind picks the right URL prefix:
    toolset -> https://wrocpp.github.io/toolset/<slug>/
    post    -> https://wrocpp.github.io/posts/<slug>/
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: PyYAML not installed. run: pip3 install pyyaml")

REPO_ROOT = Path(__file__).resolve().parent.parent
WEBHOOK_PATH = Path.home() / ".claude" / "secrets" / "wrocpp-slack-webhook"


def load_webhook() -> str:
    if not WEBHOOK_PATH.is_file():
        sys.exit(f"error: webhook secret not found at {WEBHOOK_PATH}")
    mode = WEBHOOK_PATH.stat().st_mode & 0o777
    if mode & 0o077:
        sys.exit(f"error: webhook secret at {WEBHOOK_PATH} is world/group-readable "
                 f"(mode {oct(mode)}). chmod 600 it before continuing.")
    return WEBHOOK_PATH.read_text().strip()


def find_mdx(slug: str, kind: str) -> Path:
    if kind == "toolset":
        candidate = REPO_ROOT / "src" / "content" / "toolset" / f"{slug}.mdx"
        if candidate.is_file():
            return candidate
    elif kind == "post":
        posts_dir = REPO_ROOT / "src" / "content" / "posts"
        for mdx in sorted(posts_dir.glob("*.mdx")):
            head = mdx.read_text().split("---", 2)
            if len(head) < 3:
                continue
            try:
                fm = yaml.safe_load(head[1])
            except yaml.YAMLError:
                continue
            if fm and fm.get("slug") == slug:
                return mdx
    sys.exit(f"error: no mdx found for slug={slug!r} kind={kind!r}")


def parse_frontmatter(mdx: Path) -> dict:
    parts = mdx.read_text().split("---", 2)
    if len(parts) < 3:
        sys.exit(f"error: no frontmatter in {mdx}")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        sys.exit(f"error: frontmatter is not a mapping in {mdx}")
    return fm


def build_message(fm: dict, slug: str, kind: str) -> str:
    url_prefix = "toolset" if kind == "toolset" else "posts"
    url = f"https://wrocpp.github.io/{url_prefix}/{slug}/"
    title = fm.get("title", slug)
    summary = fm.get("summary", "").strip()
    # Slack mrkdwn: <url|label> for hyperlinks; *bold* for emphasis.
    # Keep it short -- channel messages reward brevity.
    lines = [
        f":magnet: New on wro.cpp -- *<{url}|{title}>*",
        "",
        summary,
    ]
    return "\n".join(lines)


def post_to_slack(webhook: str, message: str) -> None:
    payload = json.dumps({"text": message}).encode()
    req = urllib.request.Request(
        webhook,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode()
        if body.strip() != "ok":
            sys.exit(f"error: Slack webhook returned {body!r}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--kind", required=True, choices=("toolset", "post"))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    mdx = find_mdx(args.slug, args.kind)
    fm = parse_frontmatter(mdx)
    message = build_message(fm, args.slug, args.kind)

    print("--- message ---")
    print(message)
    print("---------------")

    if args.dry_run:
        print("(dry-run, not posting)")
        return

    webhook = load_webhook()
    post_to_slack(webhook, message)
    print("posted to wro.cpp #general (webhook ok).")


if __name__ == "__main__":
    main()
