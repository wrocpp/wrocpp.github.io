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

## What the linter can and cannot catch

- **Mechanical (linter gates it):** dashes, formulaic closers, negative parallelism (flagged for
  review), punchy-fragment runs, the caption tic, significance phrases, the colon-title formula,
  generic headers, tricolon anaphora, bold volume, stock openers.
- **Human judgment only (linter is silent):** the myth->demo->catch->teaser skeleton as a whole,
  whether a "not X, but Y" is a real misconception-correction, whether the significance is genuine,
  and whether every adjective is earned. A green lint means "no obvious tells," not "good writing."
