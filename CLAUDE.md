# wrocpp.github.io project instructions

This repo is the wro.cpp publication (Astro site + social-post automation). The house writing style
is the load-bearing rule here: our posts were flagged as AI-generated on r/cpp, so prose quality is a
first-class concern, not an afterthought.

## Writing (read `docs/STYLE.md` before drafting any post or caption)

**Voice:** concrete, understated, problem-first, first person where natural. Write like a working C++
engineer explaining something they hit, not like a launch announcement. Let facts carry the weight.

**The ten tells to avoid** (budgets in parens; full do/don't in `docs/STYLE.md`):

1. Em-dash / `--` asides (<=2 per post; **0** in captions) - the worst offender.
2. Formulaic closers ("and that is the point", "the whole point") - budget 0, incl. titles.
3. Negative parallelism ("not X, it's Y") - <=1, and only to correct a real misconception.
4. The repeated skeleton (myth-bust -> demo -> "The catch" -> teaser) - vary the entry point.
5. Punchy-fragment runs; the "Live in your browser." caption tic - banned.
6. Significance-inflation ("matters most", "the strongest bid") - cut it; show, don't announce.
7. Colon-title formula (`Phrase: the X that Y`) - rotate declaratives/questions.
8. Generic headers (`## Why it matters`, `## What's next`) - name the section's content.
9. Rule-of-three anaphora ("same X, same Y, same Z") - <=1.
10. Bold overuse - budget 8; bold only term-of-art introductions.

**Gate:** run `python3 scripts/prose-lint.py --slug <slug>` (and `--caption <path>` for captions)
before publishing. ERROR blocks; WARN must be read and either fixed or justified. This runs inside the
`publish-post` and `advertise-post` skills.

## Community posting & AI disclosure

Our automation posts to the website, LinkedIn, and Facebook. Every post is labeled with its AI
disclosure (`aiDisclosure` frontmatter, the byline label, and the `/ai` page). **Never post our
AI-generated/assisted content to communities that ban it (r/cpp, r/programming, HN), and do not hand
it to anyone to post there.** This is a hard rule: human-editing it does not make it postable there.
`prose-lint` is for writing quality only; it must never be used to make AI content pass as human. See
`docs/STYLE.md` community policy and `/ai`.

## Other

- ASCII only in commit messages, PR descriptions, and scripts (no em-dashes or smart quotes; use
  parens, not dashes, for parenthetical clauses).
- Post/caption authoring and publishing mechanics live in `.claude/skills/{publish-post,advertise-post,push-to-buffer}/SKILL.md`.
