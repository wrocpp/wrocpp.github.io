# LinkedIn Square Post (1200x1200)

Standard LinkedIn feed post at 1:1 square aspect ratio. Works well as a scroll-stopping image in the LinkedIn feed.

## Usage

```bash
brand-gen init social/linkedin-post my-post
cd my-post
# edit content.md
brand-gen build      # -> index.html
brand-gen image      # -> my-post.png (2400x2400 at 2x DPR)
```

## Directives

All templates use one of four post types. Each uses the same directive pattern:

### Quote

```markdown
::::post{type=quote theme=dark logo=top-left}

:::quote{author="Filip Sajdak" role="Founder & CEO, ScudoAI"}

Sovereign AI is not a feature you bolt on later. It is the architecture.

:::

::::
```

### Stat

```markdown
::::post{type=stat theme=light accent=brand}

:::stat{value="USD 80B" label="Worldwide sovereign cloud spend" context="Europe is the fastest-growing region at 83% YoY." source="Gartner, Feb 2026"}
:::

::::
```

### Announcement

```markdown
::::post{type=announcement theme=light}

:::announcement{kind="launch" date="April 2026"}

# ScudoAI joins NVIDIA Inception

We are thrilled to join the NVIDIA Inception program to accelerate sovereign AI deployment across European regulated industries.

:::

::::
```

### Insight

```markdown
::::post{type=insight theme=dark}

:::insight{citation="EU AI Act full enforcement: 2 August 2026"}

# The AI compliance deadline most companies are missing

Full EU AI Act enforcement for high-risk AI systems begins in 2 August 2026. Most regulated enterprises are not ready for the documentation and audit requirements. Teams running cloud AI will face the hardest transition.

:::

::::
```

## Attributes reference

### `::::post` attributes

- `type` - quote | stat | announcement | insight (required)
- `theme` - dark | light (default light)
- `accent` - brand | amber | nv (optional colored gradient background)
- `logo` - top-left | top-right | bottom-left | bottom-right (default bottom-right)

### `:::quote` attributes

- `author` - attribution name (appears below the quote)
- `role` - attribution role/title (appears under the author)

### `:::stat` attributes

- `value` - the big number (e.g. "USD 80B", "3/4", "Hours to minutes")
- `label` - short label under the value
- `context` - 1-2 sentences providing context
- `source` - small citation

### `:::announcement` attributes

- `kind` - launch | milestone | event | hire | partnership
- `date` - free-form date string

### `:::insight` attributes

- `citation` - small footer citation (e.g. regulation reference)

## Character limits

- **Quote body**: ~120 characters for maximum readability at thumbnail size
- **Stat label**: ~40 characters
- **Stat context**: ~200 characters
- **Announcement headline**: ~80 characters
- **Announcement body**: ~250 characters
- **Insight hook**: ~100 characters
- **Insight body**: ~300 characters

Posts that exceed these limits will still render but typography may shrink or content may clip.

## Media

Add a `media/` directory to the project and reference local files:

```markdown
:::background{image="nvidia-thor.jpg" overlay="dark"}
:::

:::image{src="product-screenshot.png" alt="ScudoAI compliance dashboard" position="top"}
:::
```

Paths are relative to the project's `media/` directory.
