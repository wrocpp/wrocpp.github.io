---
name: publish-post
description: Ship a wro.cpp blog post end-to-end. Verifies code in the cpp26-reflection-examples repo, generates Compiler Explorer permalinks, wires them into the MDX, hand-curates cross-references to/from prior posts in the series, flips draft to false, and opens a PR with three atomic conventional commits. Pass the post slug or its series_order (e.g. "first-reflection" or "02").
argument-hint: <slug-or-NN>
disable-model-invocation: true
allowed-tools: Read Write Edit Glob Grep Bash(git *) Bash(gh *) Bash(npm *) Bash(python3 *) Bash(./verify.sh *) Bash(./cpp *) Bash(./run *) Bash(date *) Agent AskUserQuestion ToolSearch CronCreate
---

# /publish-post -- ship one wro.cpp blog post

In-flight PRs at invoke time:

```!
cd /Users/filipsajdak/dev/wrocpp.github.io && gh pr list --state open --json number,title -q '.[] | "PR#\(.number): \(.title)"'
```

Use this skill to land MR2..MR25 of the C++26 reflection series. Each invocation produces one `mr/<NN>-<slug>` PR ready for review, with all the work the per-MR checklist in `~/.claude/plans/lets-split-all-the-temporal-oasis.md` calls for.

The skill must be invoked from the wrocpp.github.io repo root.

## Preconditions

- `gh auth status` is logged in.
- `brand-gen` is on PATH (only matters if you also run `/advertise-post` afterwards).
- `python3 -c "import yaml"` succeeds (pyyaml available for the shortener).
- Working tree is clean on `main` (or you've explicitly chosen to stack on a prior MR's branch).
- `/Users/filipsajdak/dev/c++26` is checked out, on a branch with the post's example sources.

If any precondition fails, abort and explain what to fix.

## Steps (execute in order; do not skip)

### 1. Resolve the target

Accept `<slug-or-NN>` and locate the matching `src/content/posts/*.mdx`:
- If the argument is two digits or "NN-something", treat it as `series_order` and find the mdx with that frontmatter value.
- Otherwise treat the argument as the `slug:` field.

Read the frontmatter; capture `title`, `summary`, `slug`, `series`, `series_order` (= NN), `pubDate`, `tags`, `kind`. Note the post's filename so commit/branch names can use it.

If `draft: false` already, abort with "post is already shipped" -- do not re-publish.

## ! Hard rule: every post must compile in BOTH places before publish

Every post on wro.cpp tells readers the code works in two specific environments. That promise has to be held literally:

1. **Local container** -- `cd /Users/filipsajdak/dev/c++26 && ./verify.sh posts/<NN>-<slug>/` exits 0. The container is `clang-p2996:latest`, built from the pinned Bloomberg fork via `./build.sh` (one-time, ~45-90 min).
2. **Compiler Explorer** -- the godbolt shortlink generated in step 4 must open + compile + run cleanly with the pinned compiler id `clang_bb_p2996` and flags `-std=c++26 -freflection-latest -stdlib=libc++`. Manually open the URL and click "Run" (or use Chrome's headless screenshot to confirm the output panel says "Program returned: 0" with the expected stdout).

**Never skip either check, even when one is inconvenient.** If the container isn't built locally, build it first (`./build.sh`) -- don't bypass step 3 just to ship faster. If the godbolt link 404s after generation, re-shorten and re-test before merging.

These two checks are the contract with readers; everything else in this skill is plumbing.

### 2. Branch

Create branch `mr/<NN>-<slug>` from `main` (after `git pull --ff-only`). If the user said to stack on the previous MR's branch, branch from there instead.

### 3. Verify code compiles

`cd /Users/filipsajdak/dev/c++26 && ./verify.sh posts/<NN>-<slug-folder>/`

The folder slug may differ from the mdx slug for post 1 only; for everything else it's `<NN>-<filename-suffix>`. Use Glob to find the matching `posts/<NN>-*/` directory if there's any ambiguity.

Stop if any example fails. Fix the .cpp first, commit and tag in the cpp26 repo:
```
git -C /Users/filipsajdak/dev/c++26 add posts/<NN>-<slug-folder>/
git -C /Users/filipsajdak/dev/c++26 commit -m "fix(post-<NN>): ..."
git -C /Users/filipsajdak/dev/c++26 tag posts/<NN>@v1
git -C /Users/filipsajdak/dev/c++26 push --follow-tags
```

### 4. Generate Compiler Explorer permalinks (with API run-verify)

```
python3 scripts/shorten-examples.py --post <NN>-<slug-folder>
```

For every example, the script now:
1. POSTs the source to godbolt's `/api/compiler/<id>/compile` with `execute: true`. **Aborts** if the compile or program exit code is non-zero.
2. Captures `stdout` into the YAML as `expected_output:` (used by the post-merge content-drift check).
3. Shortens via the `/api/shortener` if there's no existing id (or if `--force`). Otherwise re-uses the existing id and just refreshes `expected_output` if it has drifted.

The post-2 fire-drill informed this: the local container PASS doesn't catch CE-only failures, and a working shortlink id doesn't imply the code compiles today.

`--no-run-verify` is available but you should never use it -- it disables the contract with readers.

### 5. Wire permalinks into the MDX

Open the post's `.mdx`. For every `<GodboltEmbed id="TODO..." ... />` (placeholder mode, see `src/components/GodboltEmbed.astro:31`), look up the matching `<slug>.<variant>` in the YAML and replace the `id` prop with the real shortlink id. Variant -> attribute mapping is by name (e.g. `teaser_peel` -> the embed labelled "peel-first").

Also drop any `fallbackHref` props that explicitly named the (deleted) playground repo.

### 6. Cross-reference scan (the most important step; Claude judgment)

For each prior post in the same series with `series_order < NN`:
1. Read the post fully.
2. Find every place where the **new** post N is the natural deeper-dive for a topic the prior post mentions in passing. Examples:
   - Post 1 mentions `^^` -> link to post 2 ("first reflection") at first occurrence.
   - Post 6 mentions "annotations" -> link to post 9 once it ships.
   - A post with no relevant overlap stays untouched. **Do not link for completeness.**
3. Add inline markdown links: `[<short label>](/posts/<slug>/)`. Keep prose natural -- the sentence must still read well if the link is removed.
4. Cap at 1-2 forward links per prior post. If the new post owns multiple sub-topics, prefer the most central one.

In the new post N itself:
1. Add a backward link to any prior post that owns a primitive cited in passing (e.g. post 11 references "the JSON serializer" -> link to post 8).
2. Don't add a "previous in series" sentence at the top -- the auto-generated SeriesNav at the bottom handles that.

Use `AskUserQuestion` to confirm a subset of edits if the proposed list is large (>10 link insertions across all prior posts).

### 7. Flip the publish flag

In the new post's mdx, change `draft: true` -> `draft: false`. Leave `pubDate` alone (the daily cron build at 07:00 UTC publishes on its own). Pass `--publish-now` to the skill to also bump pubDate to today and rename the file accordingly.

### 7b. Create the post's GitHub Discussion thread

Spawn a discussion thread for the new post so readers have a per-post place to ask questions. Idempotent (skipped if frontmatter already has `discussion:`).

```
python3 scripts/create-discussion.py --slug <slug>
```

The script:
- Reads the post's frontmatter.
- Looks up the godbolt id (if any) for a "try the code" link in the discussion body.
- Calls the `createDiscussion` GraphQL mutation in the `General` category.
- **Patches the mdx**: adds `discussion: <url>` to the frontmatter and rewrites any generic `https://github.com/wrocpp/wrocpp.github.io/discussions` link in the body to point at the specific thread.

The discussion link surfaces in `PostLayout`'s article meta as `· discuss` and in the post's own CTA paragraph.

### 8. Build sanity check + link sweep + drift watch

```
NODE_ENV=production npm run build
python3 scripts/check-post-links.py --slug <slug>
```

`npm run build` must complete without warnings. `check-post-links.py` greps every `href` in the new post's HTML and verifies internal links resolve in `dist/`, plus HEAD-checks external links. **Abort on any failure** -- this catches forward-refs that escaped PostLink wrapping (the failure mode where a live post has a broken link to an unshipped post).

If any internal link points to a post that hasn't shipped yet, wrap that link in `<PostLink slug="...">label</PostLink>` so it renders as plain text until the target's pubDate, then auto-becomes a live link.

### 9. Three atomic commits

In this order, on the `mr/<NN>-<slug>` branch:

```
git add src/content/posts/<date>-<slug>.mdx
git commit -m "feat(post-<NN>): publish \"<title>\" with live godbolt links

<short body explaining what the post covers>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"

git add src/data/godbolt-permalinks.yml
git commit -m "chore(data): add godbolt permalinks for post <NN>

Generated by scripts/shorten-examples.py against the pinned
clang_bb_p2996 toolchain.

Co-Authored-By: ..."

git add src/content/posts/<other-prior-posts>.mdx
git commit -m "docs(posts): cross-reference post <NN> from posts <NN-list>

Inline links added where post <NN> is the natural deeper-dive for a
topic the prior post mentions only in passing.

Co-Authored-By: ..."
```

If a step has nothing to add (e.g. no cross-refs were warranted), drop that commit.

### 10. Push, open PR, schedule pre-Buffer guard, and queue a post-merge drift check

```
git push -u origin mr/<NN>-<slug>
gh pr create --base main --head mr/<NN>-<slug> \
  --title "MR<NN>: publish post <NN> -- <title>" \
  --body "..."
```

PR body follows the template in `~/.claude/plans/lets-split-all-the-temporal-oasis.md`.

**Mandatory automated safeguards** (don't skip; the post-2 fire-drill happened because these weren't in place):

1. **Pre-Buffer publish guard.** Schedule a one-shot cron via the `CronCreate` tool to fire 15 min before the Buffer schedule time (= post's pubDate at 07:45 UTC). The cron prompt should: (a) `curl -sI` the post URL, (b) on 404, manually trigger `gh workflow run deploy.yml`, watch it to completion, re-verify, (c) on STILL 404, escalate by reading the build log and reporting. Persist with `durable: true` so it survives session restarts.

2. **Post-merge content-drift check.** After the user merges the PR (and the deploy run completes), Claude must run `python3 scripts/check-live-content.py --slug <slug>`. This catches the post-2 failure mode where the godbolt id was wired in on a branch but lost in the merge. If drift is found (TODO id in live HTML, frontmatter title/summary mismatch, missing godbolt link, etc.), open + auto-merge a hotfix PR.

3. **Discussion thread auto-create.** Before opening the PR, run `python3 scripts/create-discussion.py --slug <slug>` (idempotent: skips if frontmatter already has `discussion:`). This patches the mdx so the discussion URL is in the frontmatter + in the body's CTA before the PR opens. Future PostLayout renders show a `· discuss` link in the article meta.

Print the PR URL + the cron job id + the discussion URL. Remind the user that:
- The post stays invisible in production until `pubDate` (daily cron at 07:00 UTC).
- After merge, run `/advertise-post <slug>` to generate the LinkedIn + Facebook material.
- The pre-Buffer cron will auto-fix any cron-vs-Buffer race.

## Reuse

- `src/lib/posts.ts:16-22` -- `isPublished` gate (sanity check post visibility).
- `src/data/godbolt-permalinks.yml:1-9` -- header documents the compiler id + flags.
- `src/components/GodboltEmbed.astro:31` -- placeholder detection (`id.startsWith('TODO')`).
- `/Users/filipsajdak/dev/c++26/verify.sh` -- compile harness for one post folder.
- `scripts/shorten-examples.py --help` -- shortener usage.

## Failure modes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `verify.sh` fails | example doesn't compile | fix the .cpp in cpp26, commit there first |
| shortener returns 4xx | wrong compiler id / API down | retry; check src/data/godbolt-permalinks.yml header |
| build warns about missing TODO id | step 5 missed a GodboltEmbed | re-grep `id="TODO`, wire it |
| series prev/next bar empty in dev | filter `isPublished` excluded the post | confirm draft flip applied; restart dev server |

## Out of scope

- Posting to LinkedIn / Facebook: that's `/advertise-post`.
- Deploying: GitHub Actions runs deploy.yml on push to main and on the daily cron.
- Editing PostLayout / SeriesNav / routes: those are MR1 infrastructure, untouched after.
