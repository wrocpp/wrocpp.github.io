#!/usr/bin/env python3
"""
Push a wro.cpp social/<platform>/<slug>/ artefact to Buffer as a DRAFT.

Reads BUFFER_API_KEY from `.env` (or the environment), discovers Buffer
channels via the GraphQL API, matches LinkedIn / Facebook channels by
their `service` field, then creates a draft post (saveToDraft=true) for
each channel using the caption from `caption.md` and the image URL passed
via --image-url (must be publicly fetchable -- Buffer fetches it server-side).

Drafts land in your Buffer Drafts tab; you review + schedule manually.

Usage:
    scripts/push-to-buffer.py \\
        --slug why-cpp26-reflection-matters \\
        --image-url https://wrocpp.github.io/og/why-cpp26-reflection-matters.png \\
        [--platforms linkedin,facebook] \\
        [--linkedin-channel <id>] \\
        [--facebook-channel <id>] \\
        [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUFFER_GRAPHQL = "https://api.buffer.com"


def load_dotenv(path: Path) -> None:
    """Minimal .env loader -- one KEY=value per line, no quoting magic."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip("'").strip('"')
        os.environ.setdefault(k.strip(), v)


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        BUFFER_GRAPHQL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        out = json.loads(resp.read().decode())
    if out.get("errors"):
        sys.exit(f"buffer graphql error: {json.dumps(out['errors'], indent=2)}")
    return out["data"]


def get_organization_id(token: str) -> str:
    data = gql(token, "query { account { organizations { id name } } }")
    orgs = data["account"]["organizations"]
    if not orgs:
        sys.exit("error: no organizations on this Buffer account")
    if len(orgs) > 1:
        # Pick the first; print warning so user can override via env if needed
        names = ", ".join(f"{o['id']} ({o.get('name','?')})" for o in orgs)
        print(f"note: multiple orgs ({names}); using first", file=sys.stderr)
    return orgs[0]["id"]


def list_channels(token: str, org_id: str) -> list[dict]:
    data = gql(
        token,
        """
        query($input: ChannelsInput!) {
          channels(input: $input) { id name service displayName }
        }
        """,
        {"input": {"organizationId": org_id}},
    )
    return data["channels"] or []


def pick_channel(channels: list[dict], platform: str, override_id: str | None) -> dict | None:
    """Match a channel for a platform. `service` is something like 'linkedin',
    'linkedin_company_page', 'facebook', 'facebook_page' depending on account
    setup. We match by case-insensitive substring on `service`."""
    if override_id:
        for c in channels:
            if c["id"] == override_id:
                return c
        sys.exit(f"error: --{platform}-channel id {override_id} not in channel list")
    matches = [c for c in channels if platform.lower() in (c.get("service") or "").lower()]
    if not matches:
        return None
    if len(matches) > 1:
        names = ", ".join(f"{c['id']} ({c.get('displayName')})" for c in matches)
        print(f"note: multiple {platform} channels ({names}); using first. Override with --{platform}-channel.", file=sys.stderr)
    return matches[0]


def caption_to_post_text(caption_md: str) -> str:
    """caption.md is structured (Body / Hashtags / Alt-text / Suggested time
    sections). For the Buffer post, we want the Body + Hashtags joined with a
    blank line. Alt-text and Suggested time stay metadata-only."""
    sections: dict[str, list[str]] = {}
    current = None
    for line in caption_md.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    body = "\n".join(sections.get("body", [])).strip()
    hashtags = "\n".join(sections.get("hashtags", [])).strip()
    if not body:
        sys.exit("error: caption.md has no '## Body' section")
    return f"{body}\n\n{hashtags}".strip() if hashtags else body


CREATE_POST_MUTATION = """
mutation CreateDraft($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id status text } }
    ... on MutationError    { message }
  }
}
"""


def create_draft(token: str, channel_id: str, text: str, image_url: str) -> dict:
    return gql(
        token,
        CREATE_POST_MUTATION,
        {
            "input": {
                "text": text,
                "channelId": channel_id,
                "schedulingType": "automatic",
                "mode": "addToQueue",
                "saveToDraft": True,
                "assets": {"images": [{"url": image_url}]},
            }
        },
    )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slug", required=True, help="post slug, e.g. why-cpp26-reflection-matters")
    p.add_argument("--image-url", required=True, help="publicly-fetchable URL of the social card PNG")
    p.add_argument("--platforms", default="linkedin,facebook",
                   help="comma-separated subset of {linkedin, facebook}")
    p.add_argument("--linkedin-channel", help="override LinkedIn channel id")
    p.add_argument("--facebook-channel", help="override Facebook channel id")
    p.add_argument("--dry-run", action="store_true", help="resolve channels + show payloads, don't push")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    token = os.environ.get("BUFFER_API_KEY")
    if not token:
        sys.exit("error: BUFFER_API_KEY not set (put it in .env or export it)")

    platforms = [s.strip() for s in args.platforms.split(",") if s.strip()]
    overrides = {"linkedin": args.linkedin_channel, "facebook": args.facebook_channel}

    print("--> Discovering org + channels", file=sys.stderr)
    org_id = get_organization_id(token)
    channels = list_channels(token, org_id)
    if not channels:
        sys.exit("error: no Buffer channels connected to this org. Connect LinkedIn / Facebook first in Buffer.")
    print(f"    org={org_id}  channels={len(channels)}", file=sys.stderr)
    for c in channels:
        print(f"      - {c['id']}  service={c.get('service'):20}  display={c.get('displayName')}",
              file=sys.stderr)

    for plat in platforms:
        chan = pick_channel(channels, plat, overrides.get(plat))
        if not chan:
            print(f"skip {plat}: no matching channel", file=sys.stderr)
            continue
        cap_path = REPO_ROOT / "social" / plat / args.slug / "caption.md"
        if not cap_path.exists():
            print(f"skip {plat}: {cap_path} missing", file=sys.stderr)
            continue
        text = caption_to_post_text(cap_path.read_text())
        print(f"\n--> {plat}: channel={chan['id']} ({chan.get('displayName')})  chars={len(text)}",
              file=sys.stderr)
        if args.dry_run:
            print(text)
            print(f"    image: {args.image_url}")
            continue
        result = create_draft(token, chan["id"], text, args.image_url)["createPost"]
        if result.get("__typename") == "PostActionSuccess":
            print(f"ok   created draft post id={result['post']['id']}", file=sys.stderr)
        else:
            sys.exit(f"buffer error for {plat}: {result.get('message')}")

    if not args.dry_run:
        print("\n[ok] drafts pushed -- review them at https://publish.buffer.com/drafts", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
