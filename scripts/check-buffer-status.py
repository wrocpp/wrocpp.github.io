#!/usr/bin/env python3
"""
Verify a wro.cpp post has been sent on LinkedIn + Facebook via Buffer.

Reads BUFFER_API_KEY from `.env` (same loader as push-to-buffer.py).
Queries Buffer's GraphQL for sent posts on the wro.cpp channels and
matches against the post URL derived from --slug + --kind.

Used by the pre-Buffer cron guards to flip "trust the Buffer schedule"
into "verified the post actually fired". Exit code:
  0 = both LinkedIn and Facebook show a SENT post for this slug
  1 = at least one platform missing (still queued, paused, errored, or
      never scheduled)

Usage:
    scripts/check-buffer-status.py --slug five-uses-of-reflection --kind post
    scripts/check-buffer-status.py --slug hardened-stdlib --kind toolset
    scripts/check-buffer-status.py --slug X --kind post --window-hours 6 --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUFFER_GRAPHQL = "https://api.buffer.com"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"'))


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        BUFFER_GRAPHQL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Buffer's WAF returns 403 to bare Python-urllib UAs.
            "User-Agent": "wrocpp-check-buffer-status/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="replace")
        sys.exit(f"error: Buffer GraphQL HTTP {e.code}: {body_txt[:400]}")
    if payload.get("errors"):
        sys.exit(f"error: Buffer GraphQL: {json.dumps(payload['errors'])[:400]}")
    return payload["data"]


def get_organization_id(token: str) -> str:
    data = gql(token, "query { account { organizations { id name } } }")
    orgs = data["account"]["organizations"]
    if not orgs:
        sys.exit("error: no organizations on this Buffer account")
    return orgs[0]["id"]


def list_channels(token: str, org_id: str) -> list[dict]:
    data = gql(
        token,
        "query($input: ChannelsInput!) {\n"
        "  channels(input: $input) { id name service displayName }\n"
        "}",
        {"input": {"organizationId": org_id}},
    )
    return data["channels"] or []


def pick(channels: list[dict], platform: str) -> dict | None:
    matches = [c for c in channels if platform.lower() in (c.get("service") or "").lower()]
    if not matches:
        return None
    if len(matches) > 1:
        for c in matches:
            name = (c.get("displayName") or "").lower()
            if "wro.cpp" in name or "wrocpp" in name or "wro cpp" in name:
                return c
    return matches[0]


def sent_posts_for_channel(token: str, org_id: str, channel_id: str, since_iso: str) -> list[dict]:
    """List sent posts on a channel since ISO timestamp. Buffer's schema:
       posts(input: { organizationId, filter: { channelIds, status } }, first)
    `first` is a top-level argument; `channelIds` + `status` live under
    PostsFiltersInput. Status is a list (e.g. ["sent"]). Returns a flat
    array of Post nodes (no edge wrapper)."""
    data = gql(
        token,
        "query($input: PostsInput!, $first: Int) {\n"
        "  posts(input: $input, first: $first) {\n"
        "    edges { node { id text status sentAt updatedAt channelService } }\n"
        "  }\n"
        "}",
        {
            "input": {
                "organizationId": org_id,
                "filter": {"channelIds": [channel_id], "status": ["sent"]},
            },
            "first": 50,
        },
    )
    edges = ((data.get("posts") or {}).get("edges") or [])
    nodes = [e["node"] for e in edges]
    return [n for n in nodes if (n.get("sentAt") or "") >= since_iso]


def url_for(slug: str, kind: str) -> str:
    prefix = "toolset" if kind == "toolset" else "posts"
    return f"https://wrocpp.github.io/{prefix}/{slug}/"


def find_match(posts: list[dict], slug: str, url: str) -> dict | None:
    """Match a sent post by URL or slug substring in the post text."""
    for p in posts:
        text = (p.get("text") or "")
        if url in text or f"/{slug}/" in text:
            return p
    return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--kind", required=True, choices=("toolset", "post"))
    p.add_argument("--window-hours", type=int, default=6,
                   help="Only consider posts sent within this many hours (default 6)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    token = os.environ.get("BUFFER_API_KEY")
    if not token:
        sys.exit("error: BUFFER_API_KEY not set (expected in .env)")

    since = (datetime.now(timezone.utc) - timedelta(hours=args.window_hours)).isoformat()
    url = url_for(args.slug, args.kind)

    org_id = get_organization_id(token)
    channels = list_channels(token, org_id)

    result = {"slug": args.slug, "kind": args.kind, "url": url,
              "window_hours": args.window_hours, "platforms": {}}
    all_sent = True
    for platform in ("linkedin", "facebook"):
        ch = pick(channels, platform)
        if not ch:
            result["platforms"][platform] = {"status": "no-channel-configured"}
            all_sent = False
            continue
        posts = sent_posts_for_channel(token, org_id, ch["id"], since)
        match = find_match(posts, args.slug, url)
        if match:
            result["platforms"][platform] = {
                "status": "sent",
                "post_id": match.get("id"),
                "sent_at": match.get("sentAt"),
                "channel": ch.get("displayName"),
            }
        else:
            result["platforms"][platform] = {
                "status": "not-found",
                "channel": ch.get("displayName"),
                "considered": len(posts),
            }
            all_sent = False

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"slug={args.slug} url={url}")
        for plat, info in result["platforms"].items():
            stat = info["status"]
            extra = ""
            if stat == "sent":
                extra = f" at {info['sent_at']} (channel {info.get('channel')})"
            elif stat == "not-found":
                extra = f" (considered {info['considered']} recent sent posts on {info.get('channel')})"
            print(f"  {plat:8s}: {stat}{extra}")
        print("ok" if all_sent else "MISSING")

    sys.exit(0 if all_sent else 1)


if __name__ == "__main__":
    main()
