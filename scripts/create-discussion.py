#!/usr/bin/env python3
"""
Create one GitHub Discussion thread per wro.cpp post.

Used by /publish-post (and runnable standalone) to spawn a discussion
when a post ships, then print its URL so the post mdx can link to the
specific thread instead of the generic /discussions list.

Reads the post's frontmatter (title, slug, series, series_order) from
src/content/posts/*-<slug>.mdx, then calls the GitHub GraphQL
createDiscussion mutation. Authentication uses `gh auth token`
(re-uses the user's existing gh login -- no separate token needed).

Defaults to the "General" category. Override with --category if you
later create a custom "Posts" category in repo settings.

Usage:
    scripts/create-discussion.py --slug first-reflection
    scripts/create-discussion.py --slug first-reflection --category General
    scripts/create-discussion.py --slug first-reflection --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GH_OWNER = "wrocpp"
GH_REPO = "wrocpp.github.io"
GH_GRAPHQL = "https://api.github.com/graphql"
SITE_BASE = "https://wrocpp.github.io"


def gh_token() -> str:
    """Use the gh CLI's existing auth -- no separate PAT needed."""
    try:
        out = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        sys.exit(f"error: cannot get gh auth token: {e}. Run `gh auth login` first.")
    if not out:
        sys.exit("error: empty gh auth token")
    return out


def gql(token: str, query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        GH_GRAPHQL,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "wrocpp-create-discussion/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            out = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"github http {e.code}: {e.read().decode(errors='replace')[:500]}")
    if out.get("errors"):
        sys.exit(f"github graphql error: {json.dumps(out['errors'], indent=2)}")
    return out["data"]


def read_frontmatter(slug: str) -> dict:
    """Parse the YAML-ish frontmatter of src/content/posts/*-<slug>.mdx
    enough to grab title / pubDate / series / series_order / godbolt_id."""
    posts = sorted((REPO_ROOT / "src/content/posts").glob(f"*-{slug}.mdx"))
    if not posts:
        sys.exit(f"error: no mdx for slug {slug!r}")
    text = posts[0].read_text()
    if not text.startswith("---"):
        sys.exit(f"error: {posts[0]} has no frontmatter")
    end = text.find("\n---", 3)
    if end < 0:
        sys.exit(f"error: unterminated frontmatter in {posts[0]}")
    fm: dict = {}
    for line in text[3:end].splitlines():
        m = re.match(r'^(\w+):\s*"?([^"\n]*?)"?\s*$', line)
        if m:
            fm[m.group(1)] = m.group(2)
    if "title" not in fm:
        sys.exit(f"error: {posts[0]} missing title in frontmatter")
    return fm


def godbolt_id_for(slug: str) -> str | None:
    """Pick the first godbolt entry for the post, if any. Used to surface
    a 'try the code' link inside the discussion body."""
    yml = REPO_ROOT / "src/data/godbolt-permalinks.yml"
    if not yml.exists():
        return None
    in_post = False
    indent = None
    for line in yml.read_text().splitlines():
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" "):
            in_post = (line.rstrip(":") == slug)
            indent = None
            continue
        if not in_post:
            continue
        m = re.match(r'^(\s+)id:\s*(.+)$', line)
        if m:
            return m.group(2).strip()
    return None


def discussion_body(fm: dict, godbolt: str | None) -> str:
    title = fm["title"]
    slug = fm["slug"]
    series = fm.get("series")
    order = fm.get("series_order")
    post_url = f"{SITE_BASE}/posts/{slug}/"
    series_str = f"part {order}" if order else ""
    if series and series_str:
        series_line = f"\n**{series_str} of the [{series}]({SITE_BASE}/series/{series}/) series.**\n"
    else:
        series_line = ""
    godbolt_line = (
        f"\n- The Compiler Explorer playground: <https://godbolt.org/z/{godbolt}>\n"
        if godbolt else ""
    )
    return f"""# {title}
{series_line}
This is the discussion thread for **[{title}]({post_url})**.

**Use this thread for:**
- Questions about the code in the post
- Corrections or suggested improvements
- Your own variations / war stories

**Quick links:**
- The post: <{post_url}>{godbolt_line}- The wro.cpp series: <{SITE_BASE}/series/cpp26-reflection/>
- Slack (#wro.cpp): <https://wrocpp.slack.com>

If you spot a bug in the code or the prose, a comment here or a PR against [wrocpp.github.io](https://github.com/{GH_OWNER}/{GH_REPO}) both work.
"""


CATS_QUERY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    id
    discussionCategories(first: 25) { nodes { id name slug isAnswerable } }
  }
}
"""

CREATE_MUTATION = """
mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {repositoryId: $repoId, categoryId: $catId, title: $title, body: $body}) {
    discussion { id number url title }
  }
}
"""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slug", required=True, help="post slug, e.g. first-reflection")
    p.add_argument("--category", default="General",
                   help="discussion category name (default: General)")
    p.add_argument("--dry-run", action="store_true",
                   help="resolve ids + show payload, do not create")
    args = p.parse_args()

    fm = read_frontmatter(args.slug)
    godbolt = godbolt_id_for(args.slug)
    title = fm["title"]
    body = discussion_body(fm, godbolt)

    print(f"--> post: {title}", file=sys.stderr)
    print(f"    slug: {args.slug}", file=sys.stderr)
    if godbolt:
        print(f"    godbolt: {godbolt}", file=sys.stderr)

    token = gh_token()

    cats = gql(token, CATS_QUERY, {"owner": GH_OWNER, "name": GH_REPO})["repository"]
    repo_id = cats["id"]
    cat = next(
        (c for c in cats["discussionCategories"]["nodes"]
         if c["name"].lower() == args.category.lower()),
        None,
    )
    if not cat:
        names = ", ".join(c["name"] for c in cats["discussionCategories"]["nodes"])
        sys.exit(f"error: category {args.category!r} not found. Available: {names}")
    print(f"    category: {cat['name']} ({cat['id']})", file=sys.stderr)

    if args.dry_run:
        print("\n--- title ---")
        print(title)
        print("\n--- body ---")
        print(body)
        print("\n(dry-run; no discussion created)")
        return 0

    # Skip if the post already has a discussion URL in frontmatter --
    # avoids duplicate threads if the skill is re-run.
    if fm.get("discussion"):
        print(f"\nskip: post already has discussion: {fm['discussion']}", file=sys.stderr)
        print(fm["discussion"])
        return 0

    out = gql(token, CREATE_MUTATION, {
        "repoId": repo_id,
        "catId": cat["id"],
        "title": title,
        "body": body,
    })["createDiscussion"]["discussion"]
    discussion_url = out["url"]
    print(f"\nok   created discussion #{out['number']}", file=sys.stderr)

    # Patch the mdx: add `discussion: <url>` to the frontmatter (after the
    # `summary:` line, conventionally) AND rewrite the generic
    # /discussions link in the body to the specific thread.
    posts = sorted((REPO_ROOT / "src/content/posts").glob(f"*-{args.slug}.mdx"))
    mdx_path = posts[0]
    text = mdx_path.read_text()
    end = text.find("\n---", 3)
    fm_block, body_block = text[3:end], text[end + 4:]
    if "discussion:" not in fm_block:
        # Insert before the closing of frontmatter, after the last field.
        fm_block = fm_block.rstrip() + f'\ndiscussion: {discussion_url}\n'
    body_block = body_block.replace(
        f"https://github.com/{GH_OWNER}/{GH_REPO}/discussions",
        discussion_url,
    )
    mdx_path.write_text("---" + fm_block + "---" + body_block)
    print(f"ok   patched {mdx_path.relative_to(REPO_ROOT)}", file=sys.stderr)
    print(discussion_url)  # stdout: just the URL, easy to capture in shell
    return 0


if __name__ == "__main__":
    sys.exit(main())
