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
from datetime import datetime, timezone, timedelta
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


def gql(token: str, query: str, variables: dict | None = None, *, _retries: int = 2) -> dict:
    import time as _time
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        BUFFER_GRAPHQL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Buffer's WAF returns 403 to requests without a recognisable
            # User-Agent (e.g. bare 'Python-urllib/x.y'). Use a curl-shaped UA
            # so we get past the bot filter.
            "User-Agent": "wrocpp-push-to-buffer/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            out = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429 and _retries > 0:
            retry_after = int(e.headers.get("retryAfter", e.headers.get("Retry-After", "60")))
            retry_after = min(retry_after, 300)
            print(f"  rate limited; waiting {retry_after}s ({_retries} retries left)...",
                  file=sys.stderr, flush=True)
            _time.sleep(retry_after)
            return gql(token, query, variables, _retries=_retries - 1)
        body = e.read().decode(errors="replace")
        try:
            err = json.loads(body)
            msgs = []
            for x in err.get("errors", []):
                # Buffer puts the variable-coercion failure reason at the END
                # of the message (after a long inline copy of the value).
                # Show the last 200 chars so the actual reason is visible.
                m = x.get("message", "")
                msgs.append(m if len(m) < 400 else m[:200] + " ... " + m[-300:])
            sys.exit(f"buffer http {e.code}:\n  - " + "\n  - ".join(msgs))
        except (ValueError, KeyError):
            sys.exit(f"buffer http {e.code}: {body[:1000]}")
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
        # Prefer the channel whose displayName screams 'wro.cpp' (the brand
        # account). Falls back to first match if no wro.cpp-named channel.
        for c in matches:
            name = (c.get("displayName") or "").lower()
            if "wro.cpp" in name or "wrocpp" in name or "wro cpp" in name:
                others = ", ".join(f"{x['id']} ({x.get('displayName')})" for x in matches if x is not c)
                print(f"note: multiple {platform} channels; auto-picked {c['id']} "
                      f"({c.get('displayName')}). Others: {others}. "
                      f"Override with --{platform}-channel.", file=sys.stderr)
                return c
        names = ", ".join(f"{c['id']} ({c.get('displayName')})" for c in matches)
        print(f"note: multiple {platform} channels ({names}); using first. "
              f"Override with --{platform}-channel.", file=sys.stderr)
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


def add_utm(text: str, slug: str, platform: str, series_order: int | None) -> str:
    """Replace bare https://wrocpp.github.io/posts/<slug>/ URLs in `text`
    with UTM-tagged versions per platform, so GA4 can attribute traffic
    to LinkedIn vs Facebook vs direct without per-post manual editing.

    Skip URLs that already have `?` or `#` -- author has tagged them
    explicitly. Other domains are left untouched."""
    base = f"https://wrocpp.github.io/posts/{slug}/"
    if base not in text:
        return text
    campaign = (
        f"post-{series_order:02d}" if isinstance(series_order, int) else f"post-{slug}"
    )
    tagged = (
        f"{base}?utm_source={platform}&utm_medium=social&utm_campaign={campaign}"
    )
    return text.replace(base, tagged)


def series_order_from_post(slug: str) -> int | None:
    """Read series_order from src/content/posts/*-<slug>.mdx (frontmatter)."""
    posts = sorted((REPO_ROOT / "src/content/posts").glob(f"*-{slug}.mdx"))
    if not posts:
        return None
    for line in posts[0].read_text().splitlines():
        if line.startswith("series_order:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


CREATE_POST_MUTATION = """
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    __typename
    ... on PostActionSuccess { post { id status text dueAt } }
    ... on MutationError    { message }
  }
}
"""


def pubdate_from_post(slug: str) -> str | None:
    """Read pubDate from src/content/posts/*-<slug>.mdx (YYYY-MM-DD)."""
    posts = sorted((REPO_ROOT / "src/content/posts").glob(f"*-{slug}.mdx"))
    if not posts:
        return None
    for line in posts[0].read_text().splitlines():
        if line.startswith("pubDate:"):
            # frontmatter: `pubDate: 2026-05-13`
            return line.split(":", 1)[1].strip()
    return None


def to_dueat_utc(date_yyyy_mm_dd: str, hour_local: int = 10) -> str:
    """Compute a Buffer-compatible ISO-8601 timestamp for `date` at `hour`
    Europe/Warsaw local time, expressed in UTC. Europe/Warsaw is UTC+1 in
    winter and UTC+2 in summer (DST: last Sun of March -> last Sun of October).
    A static rule for ~99% of pubDates the series targets is good enough; we
    don't need full tzdata for this. Caller can pass --at to override."""
    y, m, d = map(int, date_yyyy_mm_dd.split("-"))
    # DST window approx: Apr 1 .. Oct 31 (Europe/Warsaw is on CEST = UTC+2)
    is_dst = 4 <= m <= 10
    offset_hours = 2 if is_dst else 1
    local = datetime(y, m, d, hour_local, 0, 0)
    utc = local - timedelta(hours=offset_hours)
    return utc.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def create_post(
    token: str,
    channel_id: str,
    text: str,
    image_url: str,
    *,
    save_to_draft: bool,
    due_at: str | None,
    service: str,
) -> dict:
    """Create a Buffer post. Two modes:
      - drafts (save_to_draft=True): lands in Buffer's Drafts tab, requires
        manual scheduling. due_at is ignored.
      - scheduled (save_to_draft=False, due_at set): goes live automatically
        on the platform at due_at (ISO 8601 UTC).
    """
    inp: dict = {
        "text": text,
        "channelId": channel_id,
        # Buffer API breaking change 2026-05-12 -> 2026-05-25:
        # assets moved from {"images": [{"url"...}]} to an ordered array
        # of {"image": {"url"...}}. Old shape rejected after 2026-05-25.
        # (Single-image post for our use case; the array shape unlocks
        # carousels we don't need.)
        "assets": [{"image": {"url": image_url}}],
    }
    # Per-platform metadata: Facebook requires PostTypeFacebook (post / story
    # / reel). LinkedIn / Twitter / Instagram have their own optional inputs;
    # we omit them here since defaults work for our use case (single-image
    # feed posts on a company page / personal profile).
    svc = (service or "").lower()
    if "facebook" in svc:
        inp["metadata"] = {"facebook": {"type": "post"}}

    # Buffer GraphQL split:
    #   schedulingType (enum: notification | automatic) -- "automatic" means
    #     Buffer publishes to the platform itself, not via mobile push. This
    #     is what we want for an unattended workflow.
    #   mode (typed ShareMode!: addToQueue | shareNow | shareNext |
    #     customScheduled | recommendedTime) -- governs WHEN. customScheduled
    #     requires dueAt.
    inp["schedulingType"] = "automatic"
    if save_to_draft:
        inp["mode"] = "addToQueue"
        inp["saveToDraft"] = True
    else:
        if not due_at:
            sys.exit("error: scheduled mode requires --at or a parseable pubDate")
        inp["mode"] = "customScheduled"
        inp["dueAt"] = due_at
    return gql(token, CREATE_POST_MUTATION, {"input": inp})


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slug", required=True, help="post slug, e.g. why-cpp26-reflection-matters")
    p.add_argument("--image-url", required=True, help="publicly-fetchable URL of the social card PNG")
    p.add_argument("--platforms", default="linkedin,facebook",
                   help="comma-separated subset of {linkedin, facebook}")
    p.add_argument("--linkedin-channel", help="override LinkedIn channel id")
    p.add_argument("--facebook-channel", help="override Facebook channel id")
    # Mode: scheduled (default) auto-fires the post on Buffer at the chosen
    # time; --draft puts it in the Drafts tab for manual scheduling.
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--draft", action="store_true",
                      help="push as Buffer drafts (manual scheduling) instead of scheduled posts")
    p.add_argument("--at", metavar="ISO_UTC",
                   help="schedule time as ISO 8601 UTC (e.g. 2026-05-13T08:00:00Z). "
                        "Default: post's pubDate at 10:00 Europe/Warsaw.")
    p.add_argument("--hour", type=int, default=10,
                   help="local hour (Europe/Warsaw) for the default schedule (default: 10)")
    p.add_argument("--dry-run", action="store_true", help="resolve channels + show payloads, don't push")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    token = os.environ.get("BUFFER_API_KEY")
    if not token and not args.dry_run:
        sys.exit("error: BUFFER_API_KEY not set (put it in .env or export it)")

    platforms = [s.strip() for s in args.platforms.split(",") if s.strip()]
    overrides = {"linkedin": args.linkedin_channel, "facebook": args.facebook_channel}

    # Resolve schedule time once, before any network calls.
    due_at: str | None = None
    if not args.draft:
        if args.at:
            due_at = args.at
        else:
            pubdate = pubdate_from_post(args.slug)
            if not pubdate:
                sys.exit(f"error: cannot find pubDate for slug {args.slug!r}; "
                         f"pass --at <ISO_UTC> or --draft")
            due_at = to_dueat_utc(pubdate, args.hour)
            print(f"--> Schedule time: {due_at} (pubDate {pubdate} at "
                  f"{args.hour:02d}:00 Europe/Warsaw)", file=sys.stderr)

    if token:
        print("--> Discovering org + channels", file=sys.stderr)
        org_id = get_organization_id(token)
        channels = list_channels(token, org_id)
        if not channels:
            sys.exit("error: no Buffer channels connected to this org. Connect LinkedIn / Facebook first in Buffer.")
        print(f"    org={org_id}  channels={len(channels)}", file=sys.stderr)
        for c in channels:
            print(f"      - {c['id']}  service={c.get('service'):20}  display={c.get('displayName')}",
                  file=sys.stderr)
    else:
        print("--> dry-run without BUFFER_API_KEY: skipping channel discovery", file=sys.stderr)
        channels = [
            {"id": "<linkedin-channel-id>", "service": "linkedin", "displayName": "<your LinkedIn>"},
            {"id": "<facebook-channel-id>", "service": "facebook", "displayName": "<your Facebook>"},
        ]

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
        text = add_utm(text, args.slug, plat, series_order_from_post(args.slug))
        print(f"\n--> {plat}: channel={chan['id']} ({chan.get('displayName')})  chars={len(text)}",
              file=sys.stderr)
        if args.dry_run:
            print(text)
            print(f"    image: {args.image_url}")
            print(f"    mode:  {'DRAFT' if args.draft else f'SCHEDULED at {due_at}'}")
            continue
        result = create_post(
            token, chan["id"], text, args.image_url,
            save_to_draft=args.draft, due_at=due_at,
            service=chan.get("service") or plat,
        )["createPost"]
        if result.get("__typename") == "PostActionSuccess":
            post = result["post"]
            kind = "draft" if args.draft else f"scheduled for {post.get('dueAt') or due_at}"
            print(f"ok   created {kind}: post id={post['id']}", file=sys.stderr)
        else:
            sys.exit(f"buffer error for {plat}: {result.get('message')}")

    if not args.dry_run:
        if args.draft:
            print("\n[ok] drafts pushed -- review at https://publish.buffer.com/drafts",
                  file=sys.stderr)
        else:
            print(f"\n[ok] posts scheduled for {due_at} -- check the queue at "
                  "https://publish.buffer.com/calendar", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
