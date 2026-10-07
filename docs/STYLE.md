# wro.cpp house style

This is the source of truth for how wro.cpp posts and social captions read. It exists because our
prose had picked up the mechanical habits of generated text, to the point an r/cpp moderator flagged
a post as AI-written. The fix is not a trick to fool a detector. It is to write the way a working C++
engineer writes when they explain something they actually hit.

**Every post and caption must pass `python3 scripts/prose-lint.py` before it ships.** The linter is a
floor, not a ceiling: a green run means you avoided the obvious tells, not that the voice is right.

## Voice in one sentence

Concrete, understated, problem-first, first person where it is natural, and confident enough to let
the facts carry the weight, the way Barry Revzin or Raymond Chen write, not the way a launch
announcement reads.

## The reader we assume

Working C++ programmers. They do not need to be told that something "matters" or is "crucial." They
need the problem, the code, and the result. If a sentence only tells the reader how to feel about the
next sentence, cut it.

## The ten tells

Each row: what to stop doing, what to do instead, and why. The linter catches most of these
mechanically; numbers 3, 4, and 6 need your own judgment.

### 1. Em-dash / double-dash asides (our worst habit)

| Don't | Do |
|---|---|
| `Reflection walks the members at compile time -- no RTTI, no macros -- and emits the code.` | `Reflection walks the members at compile time. No RTTI, no macros, and it emits the code.` |

Budget: at most 2 dash asides in a post; **zero** in a caption. Reach for a period or parentheses.
A page dense with ` -- ` is the single most recognizable generated-text signature.

### 2. Formulaic closers

| Don't | Do |
|---|---|
| `...and that is the whole point.` / `...the sharp edges documented.` | End on the fact: `The generated code is byte-identical to the hand-written version.` |

Do not end a post (or a caption, or a title) by telling the reader what the point was. Stop on the
concrete result and trust them to see it.

### 3. Negative parallelism

| Don't | Do |
|---|---|
| `flat_map is not a faster map with better marketing, it is a different data structure.` | `flat_map stores its entries in a sorted vector, so lookups are a binary search over contiguous memory.` |

State the positive claim. Keep the "not X, but Y" turn for correcting a genuine misconception, at
most once per piece.

### 4. The repeated skeleton

Our posts fell into one shape: bust a myth ("usually pitched as...", "we are trained to expect..."),
show the demo, add a "## The catch" section, close with a teaser for the next post. Vary the entry
point: start inside the failing code, with a reader's question, with a benchmark number, or with a
plain definition. If three posts in a row open the same way, a regular reader feels the template.

### 5. Punchy fragments for drama

| Don't | Do |
|---|---|
| `No exception. No assertion. Just a wrong answer.` | `Nothing threw and nothing asserted; the program simply returned the wrong number.` |

One short beat per piece is fine. A string of three-word sentences is a tell. The caption tic
"Live in your browser." is banned outright.

### 6. Significance-inflation

| Don't | Do |
|---|---|
| `This is the part most introductions skip, and it matters most.` | `Splicing is what turns a reflection back into code you can call.` |

Delete narrator phrases that assert importance: "the strongest bid," "closest to home," "matters
most," "worth more than one post." Show the thing; do not announce its weight.

### 7. Colon-headline formula

| Don't | Do |
|---|---|
| `reflect_soa: the one struct that gives you three layouts` | `One struct, three memory layouts` or a question: `Which layout wins for your workload?` |

Rotate declaratives and questions in. A `library_name:` or `std::thing` prefix with a colon is fine;
the banned shape is `Phrase: the X that Y`.

### 8. Generic section headers

| Don't | Do |
|---|---|
| `## Why it matters` / `## What's next` | `## Where the 2-3x bandwidth win comes from` |

Name a section by its actual subject so it is findable in a table of contents.

### 9. Rule-of-three anaphora

| Don't | Do |
|---|---|
| `Same struct, same fields, same order.` | `The same struct definition, reordered into parallel arrays.` |

Ordinary three-item lists are fine. The repeated-lead-word tricolon ("same X, same Y, same Z"; "no A,
no B, no C") is the version to thin out, at most once per piece.

### 10. Bold overuse

| Don't | Do |
|---|---|
| Bolding **32 bytes**, **SoA**, and **cache line** across twenty spans. | Bold only the first appearance of a term of art: **struct of arrays (SoA)**, then plain. |

A post with twenty bold spans has emphasized nothing. Budget: 8.

## Positive rules

- **Vary the rhythm.** Follow a long, qualified sentence with a short plain one. Do not run three
  fragments together, and do not run five subordinate clauses together either.
- **Earn every adjective.** "Fast" needs a number. "Clean" needs a diff. If you cannot back it, cut it.
- **Plain verbs.** "X does Y," not "X serves as / represents / acts as / stands as a Y."
- **Specificity beats hype.** "6.8 GB/s on the simdjson benchmark" beats "blazingly fast."
- **First person, sparingly.** "I hit this when..." is good. "We are trained to expect..." is not.

## Titles

Length is enforced by `scripts/check-social-title.py` (frontmatter WARN 90 / ERROR 120; social card
h1 WARN 65 / ERROR 90). On top of that, avoid the `Phrase: the X that Y` formula (tell 7). Three
rewrites:

- `std::flat_map: the container that trades inserts for lookups` -> `std::flat_map trades fast inserts for fast lookups`
- `Erroneous behavior: the end of a 40-year footgun` -> `C++26 makes an uninitialized read a defined bug`
- `mp-units: the library that puts physics in the type system` -> `Units that the compiler checks`

## Headlines and hooks

Our best-performing post so far, the C++26 erroneous-behavior short, reached about 125x our usual
impressions and 100x our usual clicks. A reader summed up why in the comments: "Looks like a
clickbait, but it's actually true." That tension, curiosity on the surface and a real payoff
underneath, is the effect to aim for. It is not achieved by overstating. It is achieved by finding
the true claim that also happens to be surprising, and letting the card promise exactly what the
post delivers.

### Two tiers: card headline vs blog title

Write two different headlines for the same post.

- **The blog title** (frontmatter `title`) stays sober and precise: a verb and a concrete claim.
  "C++26 makes an uninitialized read a defined bug." It is what the reader sees once they have
  arrived, and it has to survive a careful read.
- **The social card h1** carries the curiosity: the punchiest true framing of the same fact.
  "C++26 ends a 40-year footgun." It is what makes someone stop scrolling.

The gap between the two is the click. The rule that keeps it honest: the card headline must be
literally true and fully paid off by the post. If a reader who clicks feels tricked, the card
overreached, so rewrite it down to what the post actually proves.

### The hook toolkit

The techniques that made the footgun post land, reusable on any topic:

- **A specific number, not a vague quantifier.** "40 years," not "long-standing." "Never calls
  `new`," not "fewer allocations." A number is checkable, and checkable reads as true.
- **Reframe familiar code as the danger.** `int x;` is one line every reader has written. Showing
  that the ordinary thing is the trap is more arresting than any adjective.
- **One escalation beat.** State the stakes once, higher than expected but still true: not "you get
  a wrong value" but "the compiler may delete the branch." Earn it with the demo; do not inflate it.
- **The same input twice.** The strongest proof is identical source (or identical data) producing
  two outcomes, runnable live in the embed. It is the "actually true" half of the formula.
- **Close on the mechanism, not the moral** (tell 2). End on the concrete fact the post established.

### The guardrail

This is a lever for our own channels only. It does not change the community rule below: we do not
post to r/cpp, r/programming, or Hacker News regardless of how the headline reads. And it is not a
licence to inflate. Significance-inflation (tell 6) and formulaic drama (tell 5) are still tells. A
punchy card that the post cannot cash is worse than a plain one, because the reader feels the gap on
arrival.

## Captions vs blog body

| | Caption (LinkedIn / Facebook) | Blog body |
|---|---|---|
| Charset | ASCII only, no smart quotes | UTF-8 fine |
| Dashes | **Zero** `--` or em-dashes; use periods/parens | Budget 2 |
| Length | ~250 words (LinkedIn), ~120 (Facebook) | as long as the topic needs |
| Tics | No "Live in your browser.", no "No exception. No assertion." | same |
| Bold | None or one term | Budget 8 |

Caption rules are enforced by `prose-lint.py --caption`. Caption authoring lives in
`.claude/skills/advertise-post/SKILL.md`; blog body in `.claude/skills/publish-post/SKILL.md`.

## Community and human-review policy

The wro.cpp automation drafts prose. That is fine for our own channels (the website, LinkedIn,
Facebook), which is where the `advertise-post` / `push-to-buffer` pipeline posts.

Communities that ban AI-generated content (r/cpp, r/programming, Hacker News in practice) are
different. **We do not post there at all.** This is a hard rule, not a "rewrite it enough first" rule:
those venues do not accept human-edited AI text either, so editing does not make a post eligible. The
style guide above is for genuine writing quality on our own channels; it is **not** a tool to make AI
content pass as human, and must never be used that way. Every post we publish is labeled with its AI
disclosure (the `aiDisclosure` frontmatter field, the byline label, and the `/ai` page). If a reader
chooses to share a post in one of those communities, that is their decision, not ours.

## Readability

The ten tells are about voice. This section is about how a post is laid out and how much inline
code it carries. It exists because a read of the unpublished posts found them "a wall of text", and
a measurement of all 170 posts showed why: Fog was fine, but inline code density and long runs of
paragraphs were not. `scripts/prose-lint.py` (the `sentence-length`, `code-density`, `paragraph`,
`prose-run`, `section-length` and `in-short` checks) and `scripts/readability-report.py` enforce and
measure these rules. The `write-post` skill carries the drafting rules.

### The rules

| Rule | Level | Basis |
|---|---|---|
| Sentence over 25 words: WARN. Over 35: ERROR | linter | evidence-based (GOV.UK splits above 25; Microsoft flags above 30); the 35 ceiling is a house choice |
| Mean sentence length of a section (3+ sentences) over 20: WARN | linter | house choice |
| More than 2 code spans in one sentence: WARN. More than 4: ERROR | linter | house choice |
| More than 8 code spans per 100 prose words: WARN | linter | house choice |
| Paragraph over 120 words: WARN. Over 7 sentences: ERROR | linter | house choice (Google: short paragraphs, one idea each) |
| More than 4 prose paragraphs in a row with no heading, list, table, code block or embed: WARN | linter | house choice, from the F-pattern finding that readers scan |
| A section with over 300 prose words: WARN (a heading at least every ~250 words) | linter | house choice |
| A post over 500 prose words opens with an "In short" section of 3 to 5 bullets: WARN if missing | linter | evidence-based (inverted pyramid: the conclusion first) |
| Name the thing in words first, then show the identifier; never use an identifier as a verb or bare noun ("the `offset_of` function", not "`offset_of` it") | skill | evidence-based (Google: code in text) |
| Three or more parallel items go in a table or a short list | skill | evidence-based (NN/g: scannable structure) |
| Several identifiers belong in a code block with the explanation beside it; inline code is for single names | skill | evidence-based (split attention) |
| Fog is tracked as a trend and never gates | report | Fog is weak on C++ vocabulary and identifiers |

"Evidence-based" means a published guideline or research finding supports the direction and,
where given, the number. "House choice" means we picked the number; it can move when the data says so.
**No study exists on inline code and reading speed.** Google, Microsoft and MDN say to put code
entities in code font and set no limit, so the span limits above are ours. They were chosen from the
corpus: the 8 per 100 words WARN sits just above the reflection series median, and 2 or 4 per sentence
marks where a sentence stops being prose.

### Baseline and grandfathering

`scripts/readability-baseline.json` records every post that existed when the rules landed. For a post
listed there a finding only counts, and an ERROR only gates, when its count is worse than its entry
("must not get worse"). A post that is rewritten is removed from the baseline and is then fully
enforced; a new post is enforced from the start. Regenerate the file only through
`python3 scripts/readability-report.py --write-baseline` and review the diff.

Measured on all 170 posts (medians; spans are inline code spans):

| group | n | Fog | Fog no code | mean sent | % >25 | spans/100 | % 3+ spans | headings | max run | list items |
|---|---|---|---|---|---|---|---|---|---|---|
| cpp26-reflection series | 35 | 9.7 | 9.5 | 13.5 | 10.7 | 6.4 | 7.5 | 9.0 | 3.0 | 10.0 |
| kind: short | 98 | 10.9 | 10.8 | 16.2 | 16.1 | 3.3 | 3.3 | 3.0 | 3.0 | 0.0 |
| ub-checks-per-statement series | 4 | 10.0 | 9.9 | 15.9 | 13.2 | 10.0 | 19.8 | 5.5 | 2.5 | 6.5 |
| other flagships | 38 | 10.7 | 10.7 | 16.5 | 15.2 | 2.5 | 0.0 | 2.0 | 3.0 | 0.0 |
| published before 2026-06-01 | 18 | 9.9 | 10.0 | 13.9 | 11.1 | 4.1 | 4.8 | 6.0 | 3.0 | 8.0 |
| published from 2026-06-01 | 152 | 10.5 | 10.4 | 16.2 | 15.3 | 3.8 | 4.2 | 3.0 | 3.0 | 0.0 |
| all posts | 170 | 10.4 | 10.3 | 15.8 | 14.3 | 3.8 | 4.3 | 4.0 | 3.0 | 0.0 |

The plugin rules for commits and merge requests (45-word ceiling, a heading about every 150 words)
differ from these on purpose: post bodies are held to the stricter 35 and 250.

### Tools

- `python3 scripts/prose-lint.py --file <post.mdx>`: tells and readability findings.
- `python3 scripts/readability-report.py --slug <slug>` (also `--all`, `--group`): the metrics.
- `python3 scripts/check-rewrite-invariants.py origin/main --slug <slug>`: after a rewrite, proves
  that code blocks, numbers, URLs, MDX components, headings and frontmatter (except `summary` and
  `updatedDate`) are unchanged, and prints before/after metrics.
- An advisory hook runs the first two after every edit of a post (`.claude/settings.json`).

### Sources

- GOV.UK, clear language: https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/
- NN/g, F-shaped pattern: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- NN/g, inverted pyramid: https://www.nngroup.com/articles/inverted-pyramid/
- Google developer style, code in text: https://developers.google.com/style/code-in-text
- Google technical writing, paragraphs: https://developers.google.com/tech-writing/one/paragraphs
- Microsoft, formatting developer text elements: https://learn.microsoft.com/en-us/style-guide/developer-content/formatting-developer-text-elements

## What the linter can and cannot catch

- **Mechanical (linter gates it):** dashes, formulaic closers, negative parallelism (flagged for
  review), punchy-fragment runs, the caption tic, significance phrases, the colon-title formula,
  generic headers, tricolon anaphora, bold volume, stock openers.
- **Readability (linter gates it, against the baseline):** sentence length, code spans per sentence
  and per 100 words, paragraph size, prose runs, section length, the "In short" block.
- **Human judgment only (linter is silent):** the myth->demo->catch->teaser skeleton as a whole,
  whether a "not X, but Y" is a real misconception-correction, whether the significance is genuine,
  and whether every adjective is earned. A green lint means "no obvious tells," not "good writing."
