---
name: advertise-post
description: Generate paste-ready LinkedIn + Facebook captions plus a 2400x2400 wro.cpp-branded social card image for an already-published post. Outputs land under social/<platform>/<slug>/. Posting is manual (matches the scudoai/linkedin-posts/thesis-series workflow exactly).
argument-hint: <slug>
allowed-tools: Read Write Edit Glob Grep Bash(brand-gen *) Bash(cd *) Bash(cp *) Bash(mv *) Bash(rm *) Bash(mkdir *) Bash(file *) Bash(open *) Bash(.claude/skills/advertise-post/brand-kit/inject.sh *) AskUserQuestion
---

# /advertise-post -- generate the LinkedIn + Facebook launch material for a wro.cpp post

Most recently shipped posts (for cross-referencing context):

```!
ls /Users/filipsajdak/dev/wrocpp.github.io/src/content/posts | tail -3
```

Use this skill any time after a post has shipped. It produces:

```
social/linkedin/<slug>/
  caption.md     # paste-ready post copy + hashtags + alt-text + suggested time
  image.png      # 2400x2400 branded card
  content.md     # source for brand-gen
  config.yaml    # brand-gen project config
  assets/        # vendored CSS + logo (re-skinned for wro.cpp)

social/facebook/<slug>/   # same shape
```

The skill must be invoked from the wrocpp.github.io repo root.

## Preconditions

- `which brand-gen` returns a path. (One-time install: `cd /Users/filipsajdak/dev/scudoai/brand-kit && npm link`.)
- Working tree is clean (or you're on a dedicated `chore/social-<slug>` branch).
- The target post has `draft: false` in its frontmatter.
- `python3 scripts/check-llms-sync.py` reports OK across all toolset entries. If it fails, the post being advertised may cross-reference a toolset page whose `agentInstructions` (and therefore the per-page `/toolset/<slug>/llms.txt` an agent fetches) is stale relative to the body. Resolve the drift first: read the named entry's body and `agentInstructions` together, edit the instructions for any new claims or removed patterns, then `python3 scripts/check-llms-sync.py --update`. Do NOT just `--update` without reviewing -- the guard exists to make the review explicit.

If any precondition fails, abort and explain the fix.

## Steps (execute in order)

### 1. Resolve and read the post

Glob `src/content/posts/*-<slug>.mdx`, read its frontmatter. Capture `title`, `summary`, `pubDate`, `series`, `series_order`, `kind` (flagship / short / event-recap), `tags`, `slug`.

Refuse if `draft: true` -- this skill is for shipped posts only.

Also peek at the post body for one or two phrases that would make a good hook (look for the first H1/H2 or any sentence that reads as a headline-grade claim).

### 2. Draft both captions (Claude judgment)

Write a LinkedIn-shaped and a Facebook-shaped caption. Anatomy (mirror the thesis-series convention at `/Users/filipsajdak/dev/scudoai/linkedin-posts/thesis-series/01-sovereignty-funding-paradox/caption.md`):

```markdown
# <post title>

## Body
<1-2 line hook>

<2-3 short paragraphs: what changed, the concrete consequence, one payoff a reader can act on>

<CTA: link to the post + invitation to discuss>

## Hashtags
#cpp #cpp26 #reflection #...   (5-8 tags, ASCII only, no spaces)

## Alt-text
<one sentence describing the visual card so screen readers + low-bandwidth users get the gist>

## Suggested post time
<weekday YYYY-MM-DD>, 10:00 CET
Reason: <why that slot (audience timezone, day-of-week priors)>
```

LinkedIn caption can run longer (~250 words) and lean technical. Facebook caption should be tighter (~120 words), less jargon-heavy, more focused on the punchline. Both end with the same `https://wrocpp.github.io/posts/<slug>/` link.

**Charset:** ASCII only in caption text (no em-dashes, no smart quotes). Do NOT use `--` as a dash. End the sentence with a period, or use parentheses or a comma. Captions carry **zero** `--` (this matches the owner's global standard and is enforced by `scripts/prose-lint.py --caption`).

**Caption anti-tell rules (house style, see `docs/STYLE.md`).** Captions are the most public copy we ship and are what got flagged as AI-written on Reddit. Follow these:
- **No dash asides.** Zero `--` or em-dashes; use periods or parentheses.
- **No formulaic closer.** Do not end with "that is the point," "the whole point," or "worth remembering." End on the concrete claim, then the link.
- **No stock tics.** Never write "Live in your browser." or a drama run like "No exception. No assertion." These are burned; vary or drop them.
- **At most one "Not X, but Y,"** and only to correct a genuine misconception.
- **Minimal bold.** None, or a single term of art. Captions do not need emphasis.
- **Voice:** concrete and understated (see `docs/STYLE.md#voice-in-one-sentence`), not a launch announcement.

Show the user both drafts via `AskUserQuestion` (or print + ask for "ok"); apply edits in place if requested before continuing.

### 3. Pick the post-type directive

`brand-gen` social-post supports 4 types. Choose based on the post's character:

| Post shape | Directive | Why |
| --- | --- | --- |
| Argument / "this changes the field" | `insight` | Heading + body + citation; reads as an essay teaser |
| One-line punchy claim | `quote` | Big quote mark + 1-line statement |
| A standout metric ("60-line container", "40-line JSON") | `stat` | Big value + label + 1-line context |
| Launch / first post in a series | `announcement` | Kind badge + headline + body |

When in doubt for a flagship post, pick `insight`.

### 4. Scaffold both projects with brand-gen

For each platform in {linkedin, facebook}:

```
brand-gen init social/linkedin-post social/<platform>/<slug> --dir .
```

(Both LinkedIn and Facebook use the same square 1200x1200 template; Facebook accepts the same aspect.)

This creates `social/<platform>/<slug>/{content.md, config.yaml, assets/{scudoai.css, layout.css, logo-symbol.svg}, media/}`.

### 5. Re-skin to wro.cpp -- DO NOT do this manually

The re-skin (CSS + logo swap) happens INSIDE step 9 via `inject.sh`. Do
NOT manually `cat >>` or `cp` here -- earlier versions of this SKILL.md
told you to. That approach is wrong: `cat >>` appends instead of
replacing, leaving the file with both the ScudoAI defaults and the
wro.cpp overrides, and `cp` of the logo SVG to assets/ gets ignored
because brand-gen inlines a different SVG into index.html that has to
be patched there. **The single source of truth is `inject.sh`, run in
step 9 between `brand-gen build` and `brand-gen image`.** Skip ahead.

### 6. Write the brand-gen content.md

Replace `social/<platform>/<slug>/content.md` with a one-card composition keyed on the type chosen in step 3. Templates (use the right one):

**insight:**
```markdown
---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- <pubDate-YYYY-MM-DD>"}
# <hook headline -- see step 6b for length limits>
<1-2 sentence sub-claim drawn from the post's summary>
:::

::::
```

**quote:**
```markdown
::::post{type=quote theme=dark logo=top-left}
:::quote{author="<author>" role="wro.cpp"}
<1-line zinger from the post>
:::
::::
```

**stat:**
```markdown
::::post{type=stat theme=dark accent=brand logo=top-left}
:::stat{value="60 lines" label="dependency injection" context="..." source="wro.cpp/<slug>"}
:::
::::
```

**announcement:**
```markdown
::::post{type=announcement theme=dark logo=top-left}
:::announcement{kind=launch date="<pubDate-YYYY-MM-DD>"}
# <title>
<1-2 sentence body>
:::
::::
```

Use `theme=dark` for all wro.cpp social posts (matches the thesis-series default). LinkedIn and Facebook can carry the same content.md, or be subtly different (e.g. a tighter Facebook headline). Default to identical unless the user asked to differentiate.

### 6a. Card headline: punchy but true (the two-tier rule)

The card h1 is **not** the blog title. See `docs/STYLE.md` "Headlines and hooks." The blog `title`
frontmatter stays sober and precise (verb + concrete claim); the card h1 carries the curiosity, the
punchiest framing of the same fact that is still literally true. The gap between them is the click,
and the post must pay off the card.

Derive the card h1 like this:

- Start from the single most surprising **true** fact in the post.
- Sharpen with the hook toolkit: a specific number, ordinary code reframed as the trap, one
  escalation beat. `C++26 ends a 40-year footgun`, not `New behavior for uninitialized reads`.
- **Self-check before you render:** is the card headline literally true, and does the post prove it?
  If a reader who clicks would feel tricked, dial it back to what the demo shows.

Never inflate to fill the gap (tells 5 and 6 still apply), and this lever is for our own channels
only (never r/cpp / r/programming / HN, see the community reminder in step 10).

### 7. Update config.yaml metadata

Edit `social/<platform>/<slug>/config.yaml`:

```yaml
template: social/linkedin-post

size:
  width: 1200
  height: 1200
  dpr: 2

project:
  name: "<slug>"
  author: "wro.cpp -- Wroclaw C++ community"
  email: "office@wro.cpp"
  date: "<pubDate-YYYY-MM-DD>"
```

### 7b. Validate title length for social card

After writing content.md, count the h1 line's character length and check
for any single un-breakable word longer than ~13 chars (snake_case
identifiers like `reflect_llmschema:` are the usual culprit since they
do not wrap). Either constraint forces a rewrite:

| H1 constraint | Action |
|---------------|--------|
| <= 60 chars AND no word > 13 chars | OK at default 92pt |
| Otherwise | REWRITE the headline shorter and move the long identifier into the subtitle, where it renders at 30pt and hyphenates normally |

**Do NOT try `{.title-long}` markdown directive syntax.** brand-gen's
remark parser does NOT recognise it and will render the literal text
`{.title-long}` as part of the h1. Verified on 2026-06-07 with the
reflect-llmschema card. If a smaller font is genuinely needed, edit
the rendered `index.html` between `brand-gen build` and `brand-gen image`
to add `class="title-long"` to the `<h1>` directly. Easier: shorten
the headline.

Example of a workable rewrite:
- BAD (overflows + bare-word does not wrap):
  `# reflect_llmschema: C++ functions to LLM tool-use schemas`
- GOOD (short headline, identifier moved to subtitle):
  `# C++ to LLM tool-use schemas, at compile time`
  with the library name `reflect_llmschema` mentioned in the subtitle.

You can also run the standalone check:
```bash
python3 scripts/check-social-title.py
```

### 8. Write caption.md

Drop the caption from step 2 into `social/<platform>/<slug>/caption.md` (LinkedIn copy in the linkedin/ folder, Facebook copy in the facebook/ folder).

Then run the prose-lint gate on both captions:

```bash
python3 scripts/prose-lint.py --caption social/linkedin/<slug>/caption.md
python3 scripts/prose-lint.py --caption social/facebook/<slug>/caption.md
```

An ERROR (a `--`, a stock tic, a formulaic closer) **blocks** the card build. Fix the caption text and re-run until both exit 0. A WARN means read the flagged line and decide. See `docs/STYLE.md`.

### 9. Build -> INJECT -> image  (the inject step is MANDATORY)

> **CRITICAL**: the order is `build` -> `inject.sh` -> `image`. If you
> swap the order, omit `inject.sh`, or run anything else between them,
> the rendered PNG carries the **ScudoAI shield** instead of the
> **wro.cpp magnet** and ships with ScudoAI's default CSS. This is a
> silent failure -- no warning, no error. You only notice when you
> look at the image after deploy. Two readers have already hit this
> (sanitizers-2026 + vector-consteval-or-constexpr, both shipped with
> the wrong logo and had to be re-rendered).

What each step does:

1. **`brand-gen build`** generates `index.html` with the default
   ScudoAI shield SVG inlined and `assets/scudoai.css` copied from
   the brand-kit defaults.
2. **`inject.sh`** REPLACES `assets/scudoai.css` with `wrocpp.css`
   (standalone wro.cpp stylesheet, NOT an append), blanks
   `assets/layout.css`, patches the inlined `<symbol id="scudo-logo">`
   in `index.html` with the wro.cpp magnet SVG, and stamps an
   `<div class="ai-badge">AI-generated</div>` (bottom-right AI disclosure
   label, styled by `.ai-badge` in `wrocpp.css`; see the `/ai` page). All
   operations are idempotent.
3. **`brand-gen image`** runs headless Chrome on the (now wro.cpp-skinned)
   `index.html` and writes a PNG.

Run the full sequence per platform:

```bash
for plat in linkedin facebook; do
    ( cd social/$plat/<slug> \
      && brand-gen build \
      && bash $(git rev-parse --show-toplevel)/.claude/skills/advertise-post/brand-kit/inject.sh . \
      && brand-gen image )
    mv social/$plat/<slug>/<slug>.png social/$plat/<slug>/image.png
done
```

After both platforms render, **verify the swap actually happened**:

```bash
# MUST find viewBox="0 0 320 320" -- that is the wro.cpp magnet.
# If it shows viewBox="0 0 512 512" -> inject.sh did not run; the SVG
# is still the ScudoAI shield. STOP and re-run the sequence.
grep -o 'viewBox="0 0 [0-9 ]*"' social/linkedin/<slug>/index.html | head -1

# MUST report ~340 lines (wrocpp.css standalone). If 0, the assets
# directory was empty when Chrome rendered -> giant logo bug.
# If ~1189, you appended instead of replacing -- delete the file and
# re-run inject.sh.
wc -l social/linkedin/<slug>/assets/scudoai.css

# MUST find the AI-disclosure badge. If missing, inject.sh step 3 did
# not run (or the </section> anchor was absent) -- re-run the sequence.
grep -q 'class="ai-badge"' social/linkedin/<slug>/index.html && echo "ai-badge ok"
```

PNG sanity checks (all bundled into one script):

```bash
# Runs the full render-integrity check: image dimensions, file size,
# assets/scudoai.css presence + line count, logo-symbol.svg presence,
# and a title-area pixel sample. Exits non-zero on any ERROR.
python3 scripts/check-social-render.py --slug <slug>
```

The script catches the **"giant magnet logo, no CSS"** failure mode that
shipped a broken lifetime-safety-2026 card on 2026-06-01: when Chrome
renders the index.html with an empty `assets/` directory, the magnet PNG
expands to fill the entire 2400x2400 card and the title text falls
back to default browser styles. The PNG file size jumps from ~210 KB
(correct) to ~450 KB (broken). The script flags any file outside the
150-400 KB band as suspect and verifies assets/scudoai.css matches the
300-line wrocpp.css standalone.

If the script reports ERROR for a card, the fix is always the same:
delete the card directory and re-init from scratch:

```bash
# Save content first, then nuke + re-init + restore + rebuild
cp social/linkedin/<slug>/{content.md,config.yaml,caption.md} /tmp/
rm -rf social/linkedin/<slug>
brand-gen init social/linkedin-post social/linkedin/<slug> --dir .
cp /tmp/{content.md,config.yaml,caption.md} social/linkedin/<slug>/
( cd social/linkedin/<slug> \
  && brand-gen build \
  && bash $(git rev-parse --show-toplevel)/.claude/skills/advertise-post/brand-kit/inject.sh . \
  && brand-gen image )
mv social/linkedin/<slug>/<slug>.png social/linkedin/<slug>/image.png
```

After the script passes, do the final visual check:

```bash
open social/linkedin/<slug>/image.png
```

If the logo zone check warns, either shorten the title or apply
`.title-long` / `.title-xlong` (see step 7b), then re-run the
build -> inject -> image sequence.

### 9b. Publish the image at a public URL

Buffer's API needs a publicly fetchable image URL (no base64 / no upload endpoint). The site's `public/` folder ships every file under it to https://wrocpp.github.io/, so:

```bash
mkdir -p public/og
cp social/linkedin/<slug>/image.png public/og/<slug>.png
```

After the next merge + deploy.yml run, the image is live at `https://wrocpp.github.io/og/<slug>.png` and `/push-to-buffer <slug>` can fetch it. (LinkedIn and Facebook share the same image; we only publish one.)

### 10. Print the result + reminders

Print:
- Both `caption.md` paths.
- Both `image.png` paths.
- Suggested post times (from caption.md).
- A 1-line reminder: "Manual posting: copy caption + upload image to LinkedIn / Facebook page."
- A community reminder: "These captions are for LinkedIn / Facebook automation only. NEVER post this content to r/cpp, r/programming, or other communities that ban AI-generated content, and do not hand it to anyone to post there on our behalf. Human-editing it does not make it postable there. See `docs/STYLE.md` community policy and the `/ai` page."

Do NOT post anywhere. The skill stops here.

### 11. Commit (optional, ask first)

If the user wants the artefacts committed, propose a single commit:

```
chore(social): publish <slug> launch material

LinkedIn + Facebook caption + branded image, ready for manual posting.
Generated by /advertise-post.
```

Otherwise leave the working tree dirty for the user to inspect.

## Reuse

- `/Users/filipsajdak/dev/scudoai/brand-kit/` -- the `brand-gen` CLI and the `social/linkedin-post` render template.
- `.claude/skills/advertise-post/brand-kit/wrocpp.css` -- token overrides.
- `.claude/skills/advertise-post/brand-kit/logo-symbol.svg` -- magnet mark.
- `social/README.md` -- explains the layout for downstream readers.

## Failure modes

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `brand-gen: command not found` | not installed | `cd /Users/filipsajdak/dev/scudoai/brand-kit && npm link` |
| logo renders as ScudoAI shield | step 5 didn't copy the wro.cpp logo-symbol.svg | re-run step 5 |
| watermark text says "ScudoAI" | wrocpp.css wasn't appended | re-check step 5; confirm `.logo-wordmark { font-size: 0 }` rule reaches the page |
| image is blank | brand-gen image needs Chrome at /Applications/Google Chrome.app | install Chrome or set CHROME_PATH env var |
| Fonts wrong (Outfit instead of Quicksand) | google-fonts blocked / network issue | retry; check that wrocpp.css's @import resolved |

## Out of scope

- API posting to LinkedIn / Facebook: deliberately not automated.
- Carousel or multi-slide posts: this skill only handles single-card 1200x1200.
- Banner / portrait variants: future skill if needed.
