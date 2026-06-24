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


def _resolve_webhook_path() -> Path:
    """Locate the Slack webhook secret.

    This is a Scudo-account project, so the secret normally lives under
    ~/.claude-scudo/secrets/. Fall back to the default ~/.claude/secrets/
    for environments that keep it there. The default path drives the
    "not found" error message when neither exists.
    """
    candidates = [
        Path.home() / ".claude-scudo" / "secrets" / "wrocpp-slack-webhook",
        Path.home() / ".claude" / "secrets" / "wrocpp-slack-webhook",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return candidates[-1]


WEBHOOK_PATH = _resolve_webhook_path()


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


def verify_live(url: str, title: str) -> None:
    """Refuse to post unless the URL returns 200 AND the title appears in the
    page body. The title check guards against deploy-pipeline edge cases
    where a stale CDN cache or fallback page returns 200 with the wrong
    content. Astro is static-site so there's no SPA-fallback risk, but the
    extra check costs nothing.
    """
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                sys.exit(f"error: {url} returned HTTP {resp.status}; refusing to post")
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        sys.exit(f"error: {url} returned HTTP {e.code}; refusing to post")
    except urllib.error.URLError as e:
        sys.exit(f"error: cannot reach {url} ({e.reason}); refusing to post")
    # The title is HTML-escaped in the rendered page; check for a robust
    # substring rather than the full title (titles often contain --, &, etc).
    needle = title.split(" -- ")[0].split(":")[0].strip()
    if needle and needle not in body:
        sys.exit(f"error: {url} returned 200 but title fragment {needle!r} "
                 f"not found in body; deploy may be stale -- refusing to post")


def post_to_slack(webhook: str, message: str) -> None:
    # Slack quirk: the "Customize Name / Customize Icon" settings on the
    # webhook config page are honored only by legacy Custom Integrations,
    # and even then only if the payload does NOT override them. Modern
    # app-based webhooks post as "incoming-webhook" regardless of the UI.
    # Sending username + icon_emoji explicitly is the robust path: it
    # works on classic webhooks and is harmless when the app type ignores
    # it (Slack returns the same `ok` either way).
    # Note: NO icon_emoji / icon_url override -- that would replace the
    # custom wro.cpp logo uploaded in the webhook's Customize Icon
    # setting. Username is sent explicitly because the modern app-based
    # webhook ignores the Customize Name field, but the configured icon
    # IS honored as long as the payload doesn't override it.
    payload = json.dumps({
        "text": message,
        "username": "Wro.cpp News",
    }).encode()
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
    p.add_argument("--skip-verify", action="store_true",
                   help="emergency override: skip the live-URL check (default: verify)")
    args = p.parse_args()

    mdx = find_mdx(args.slug, args.kind)
    fm = parse_frontmatter(mdx)
    message = build_message(fm, args.slug, args.kind)
    url_prefix = "toolset" if args.kind == "toolset" else "posts"
    url = f"https://wrocpp.github.io/{url_prefix}/{args.slug}/"
    title = fm.get("title", args.slug)

    print("--- message ---")
    print(message)
    print("---------------")

    if args.dry_run:
        print("(dry-run, not posting)")
        return

    if args.skip_verify:
        print("(skip-verify, NOT checking live URL)")
    else:
        verify_live(url, title)
        print(f"verified live: {url}")

    webhook = load_webhook()
    post_to_slack(webhook, message)
    print("posted to wro.cpp #general (webhook ok).")


if __name__ == "__main__":
    main()
