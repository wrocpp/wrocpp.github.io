#!/usr/bin/env python3
"""Schedule the next ready-but-unscheduled wro.cpp post onto Buffer, if a
queue slot is free.

Buffer caps each channel at 10 scheduled posts. As each day's post fires
(becomes `sent`), one slot frees. This script is meant to run once each
morning (after the 08:00Z fire): it finds the earliest future post/toolset
entry that is fully prepared (OG image + both social cards + captions) and
NOT already queued, and schedules it at <date>T08:00:00Z on both channels.

Safe to run repeatedly: it dedups against what's already on Buffer, and
does nothing when the queue is full or no candidate is ready.

  scripts/auto-schedule-next.py            # schedule the next one (if room)
  scripts/auto-schedule-next.py --dry-run  # show what it WOULD do
  scripts/auto-schedule-next.py --all      # fill every free slot, not just one

Reads BUFFER_API_KEY from .env (same loader as the sibling scripts).
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUFFER = "https://api.buffer.com"
CAP = 10


def load_env() -> None:
    f = REPO / ".env"
    if not f.exists():
        return
    for line in f.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'").strip('"'))


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        BUFFER, data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                 "Accept": "application/json", "User-Agent": "wrocpp-auto-schedule/1.0"},
        method="POST")
    with urllib.request.urlopen(req, timeout=25) as r:
        d = json.loads(r.read().decode())
    if d.get("errors"):
        sys.exit(f"error: Buffer GraphQL: {json.dumps(d['errors'])[:300]}")
    return d["data"]


def channels(token: str):
    org = gql(token, "query{ account{ organizations{ id } } }")["account"]["organizations"][0]["id"]
    chs = gql(token, "query($i: ChannelsInput!){ channels(input:$i){ id service displayName } }",
              {"i": {"organizationId": org}})["channels"] or []
    want = {}
    for svc in ("linkedin", "facebook"):
        m = [c for c in chs if c["service"] == svc and "Wro" in (c.get("displayName") or "")]
        if m:
            want[svc] = m[0]["id"]
    return org, want


def scheduled(token: str, org: str, channel_id: str) -> list[dict]:
    d = gql(token,
            "query($input: PostsInput!, $first: Int){ posts(input:$input, first:$first){"
            " edges{ node{ id text status dueAt } } } }",
            {"input": {"organizationId": org,
                       "filter": {"channelIds": [channel_id], "status": ["scheduled", "sending"]}},
             "first": 50})
    return [e["node"] for e in ((d.get("posts") or {}).get("edges") or [])]


def queued_slugs(posts: list[dict]) -> set[str]:
    out = set()
    for p in posts:
        for m in re.finditer(r"/(?:posts|toolset)/([a-z0-9-]+)/", p.get("text") or ""):
            out.add(m.group(1))
    return out


def frontmatter_field(path: Path, field: str) -> str | None:
    for line in path.read_text().splitlines()[:40]:
        if line.startswith(f"{field}:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def candidates(today: str) -> list[tuple[str, str, str]]:
    """Return (date, slug, kind) for every prepared, future, non-draft entry."""
    out = []
    for path in sorted((REPO / "src/content/posts").glob("*.mdx")):
        slug = frontmatter_field(path, "slug")
        date = frontmatter_field(path, "pubDate")
        draft = (frontmatter_field(path, "draft") or "false").lower()
        if slug and date and date >= today and draft != "true":
            out.append((date, slug, "post"))
    for path in sorted((REPO / "src/content/toolset").glob("*.mdx")):
        slug = frontmatter_field(path, "slug")
        date = frontmatter_field(path, "launchDate")
        if slug and date and date >= today:
            out.append((date, slug, "toolset"))
    return sorted(out)


def is_prepared(slug: str) -> bool:
    return all([
        (REPO / f"public/og/{slug}.png").exists(),
        (REPO / f"social/linkedin/{slug}/image.png").exists(),
        (REPO / f"social/linkedin/{slug}/caption.md").exists(),
        (REPO / f"social/facebook/{slug}/image.png").exists(),
        (REPO / f"social/facebook/{slug}/caption.md").exists(),
    ])


def due_at(date: str) -> datetime:
    return datetime.strptime(date + "T08:00:00+0000", "%Y-%m-%dT%H:%M:%S%z")


def push(slug: str, date: str, dry: bool) -> bool:
    at = f"{date}T08:00:00Z"
    url = f"https://wrocpp.github.io/og/{slug}.png"
    cmd = ["python3", str(REPO / "scripts/push-to-buffer.py"),
           "--slug", slug, "--image-url", url, "--at", at]
    if dry:
        print(f"  DRY-RUN would run: {' '.join(cmd)}")
        return True
    print(f"  scheduling {slug} at {at}")
    # Do NOT check=True: a single push failure must not abort the run.
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        print(f"  ERROR: push-to-buffer failed for {slug} (exit {r.returncode})")
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--all", action="store_true", help="fill every free slot, not just one")
    args = ap.parse_args()

    load_env()
    token = os.environ.get("BUFFER_API_KEY")
    if not token:
        sys.exit("error: BUFFER_API_KEY not set (expected in .env)")

    org, chans = channels(token)
    if set(chans) != {"linkedin", "facebook"}:
        sys.exit(f"error: expected linkedin+facebook Wro.cpp channels, found {list(chans)}")

    ln = scheduled(token, org, chans["linkedin"])
    fb = scheduled(token, org, chans["facebook"])
    free = CAP - max(len(ln), len(fb))
    already = queued_slugs(ln) | queued_slugs(fb)
    print(f"queue: linkedin={len(ln)}/{CAP} facebook={len(fb)}/{CAP} free={free}")
    if free <= 0:
        print("no free slot -- nothing to do")
        return 0

    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    # Only entries whose 08:00Z fire time is still in the FUTURE -- a post
    # dated today that already fired is gone from the queue but would still
    # match date>=today; scheduling it at a past dueAt makes Buffer reject it.
    ready = [(d, s, k) for (d, s, k) in candidates(today)
             if s not in already and is_prepared(s) and due_at(d) > now]
    if not ready:
        print("no prepared, unscheduled future post -- nothing to do")
        return 0

    print("next ready:", ", ".join(f"{d} {s}" for d, s, _ in ready[: free if args.all else 1]))
    n = free if args.all else 1
    for date, slug, _kind in ready[:n]:
        push(slug, date, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
