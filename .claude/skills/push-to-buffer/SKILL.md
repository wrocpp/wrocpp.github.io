---
name: push-to-buffer
description: Push the LinkedIn + Facebook captions + social card image for a wro.cpp post to Buffer. Default mode schedules at the post's pubDate at 10:00 Europe/Warsaw; --draft pushes to the Drafts tab for manual scheduling instead. Reads the post artefacts produced by /advertise-post.
argument-hint: <slug>
disable-model-invocation: true
allowed-tools: Read Edit Bash(python3 scripts/push-to-buffer.py *) Bash(curl *) Bash(gh *) AskUserQuestion
---

# /push-to-buffer -- create Buffer drafts for one post

Use AFTER `/advertise-post <slug>` has produced the artefacts under `social/<platform>/<slug>/`. This skill creates ONE draft per platform on Buffer; you review + schedule them in the Buffer UI.

## Preconditions

- `BUFFER_API_KEY` is set, either:
  - in a local `.env` file at the repo root (gitignored), one line: `BUFFER_API_KEY=YOUR_PERSONAL_KEY`, OR
  - exported in the shell.
  Get a personal key from https://publish.buffer.com/developers/apps (button "+ New Key").
- `social/linkedin/<slug>/caption.md` exists (Body + Hashtags sections).
- `social/facebook/<slug>/caption.md` exists.
- The social card PNG is reachable at a **public URL**. The convention this skill expects: `https://wrocpp.github.io/og/<slug>.png`. `/advertise-post` copies the image to `public/og/<slug>.png` so a `git push -> deploy.yml` cycle exposes it at that URL.

If any precondition fails, abort and tell the user how to fix.

## Steps

### 1. Confirm the image is live

```bash
curl -sI "https://wrocpp.github.io/og/<slug>.png" | head -1
```

Expect HTTP 200 with `content-type: image/png` and a `content-length` of ~hundreds of KB. If it returns 404 or the LFS-pointer length (~130 bytes), the image hasn't deployed yet -- merge the social PR first, wait ~30s for the deploy run, then re-try.

### 2. Push

```bash
python3 scripts/push-to-buffer.py \
  --slug <slug> \
  --image-url "https://wrocpp.github.io/og/<slug>.png"
```

The script:
1. Loads `BUFFER_API_KEY` from `.env`.
2. Discovers the user's organization id via `query { account { organizations { id } } }`.
3. Lists channels via `query { channels(input: { organizationId: ... }) { id name service displayName } }`.
4. Matches the LinkedIn channel by `service` containing "linkedin", same for "facebook". Override with `--linkedin-channel <id>` / `--facebook-channel <id>` if there are multiple matches (e.g. personal LinkedIn + LinkedIn company page).
5. For each platform, reads `social/<platform>/<slug>/caption.md`, joins the `## Body` and `## Hashtags` sections (drops the metadata-only `## Alt-text` and `## Suggested post time` sections), and POSTs `createPost` with `saveToDraft: true`, `assets: { images: [{ url: ... }] }`.
6. Prints the resulting draft post ids.

### 3. Review in Buffer

Open https://publish.buffer.com/drafts -- two new drafts appear (one per channel). Visually verify:
- Caption renders with line breaks intact.
- Hashtags appear as one block at the end.
- Image preview matches the wro.cpp brand card.

Schedule each draft from the Buffer UI for the time recommended in `caption.md`'s `## Suggested post time` section.

### 4. Optional: dry-run first

```bash
python3 scripts/push-to-buffer.py --slug <slug> --image-url <url> --dry-run
```

Resolves channels and prints the assembled post text + image URL without hitting `createPost`. Useful for sanity-checking the channel match.

## Reuse

- `scripts/push-to-buffer.py` -- the load-bearing CLI.
- `social/<platform>/<slug>/caption.md` -- the source of truth for post text. Edit this file (NOT in Buffer) if you want to tweak before pushing.
- `public/og/<slug>.png` -- the public copy of the social image. `/advertise-post` writes here.

## Failure modes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `BUFFER_API_KEY not set` | `.env` missing or token not exported | Create `.env` with `BUFFER_API_KEY=...`; confirm `.gitignore` excludes `.env` (it does). |
| `no Buffer channels connected to this org` | LinkedIn / Facebook not connected in Buffer | Connect them in https://publish.buffer.com -> Connect a channel. |
| `no matching channel` for a platform | service string is non-standard (e.g. "linkedin_company_page") | Run `--dry-run` to print the channel list with `service` strings. Pass `--linkedin-channel <id>` to override. |
| Buffer error "image fetch failed" | `--image-url` not publicly reachable | Re-check step 1 (curl). For a brand-new post, the public URL only goes live after the deploy.yml run. |
| Wrong post text in draft | caption.md missing `## Body` or `## Hashtags` headings | Edit caption.md to add them. The skill cares about exact `## ` (level-2) headings. |

## Out of scope

- Scheduling: Buffer drafts are NOT scheduled by this skill. You schedule manually in the UI.
- Deleting / updating drafts: re-running `/push-to-buffer <slug>` creates NEW drafts; it doesn't dedupe. Delete the old ones in Buffer if needed.
- Image hosting alternatives (imgur, S3): not implemented. The site itself hosts the OG card.
