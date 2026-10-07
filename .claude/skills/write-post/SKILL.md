---
name: write-post
description: Draft or rewrite the body of a wro.cpp post (.mdx) so it is easy to read - outcome first, an "In short" block, short sentences, little inline code, headings by subject. Use whenever writing or rewriting a post body, before publish-post or advertise-post. Rules and numbers live in docs/STYLE.md, section Readability.
argument-hint: <slug>
allowed-tools: Read Write Edit Glob Grep Bash(python3 *) Bash(git *)
---

# /write-post -- draft or rewrite one post body

Voice rules (the ten tells) are in `docs/STYLE.md`. This skill adds the layout rules from its
"Readability" section. Numbers there are the source of truth; the summary below is for drafting.

## Drafting rules

1. **Outcome first.** The opening says what the reader gets or what was found, with the number.
2. **"In short" block.** Posts over 500 prose words open with `## In short` and 3 to 5 bullets.
3. **One idea per sentence.** Aim for 15 to 20 words; split above 25 (WARN), never pass 35 (ERROR).
4. **Verb-led sentences.** Subject, verb, object. Cut "it is worth noting that" and stacked clauses.
5. **Define, then name.** Say what the thing does in words, then show the identifier once.
6. **Example before abstraction.** Show the code or the numbers, then state the rule.
7. **Table for parallel items.** Three or more parallel items go in a table or a short list.
8. **Code block beside its explanation.** Several identifiers in one statement go in a fenced block
   with the explanation next to it. Inline code is for single names.
9. **One identifier per sentence where possible.** More than 2 spans in a sentence is a WARN, more
   than 4 an ERROR, more than 8 per 100 prose words a WARN for the post.
10. **Never use an identifier as a verb or bare noun.** Write "the `offset_of` function", not
    "`offset_of` the member".
11. **Headings by subject.** A heading at least every ~250 words, no run of more than 4 prose
    paragraphs, paragraphs under 120 words and 7 sentences. Name sections by content, not "The catch".

## Rewriting an existing post

Rewrite wording only. Do not touch fenced code, numbers, URLs, `<GodboltEmbed>` / `<PostLink>`
tags and props, existing heading text, or frontmatter (except `summary` and `updatedDate`). Remove
the slug from `scripts/readability-baseline.json` once the post is rewritten, so it is fully enforced.

## Self-check before you hand the post back

```bash
python3 scripts/prose-lint.py --file src/content/posts/<file>.mdx      # no ERROR; read each WARN
python3 scripts/readability-report.py --slug <slug>                    # spans/100 <= 8, run <= 4, In short
python3 scripts/check-rewrite-invariants.py origin/main --slug <slug>  # rewrites only: must exit 0
```

Checklist:

- [ ] Opening gives the outcome, with the number.
- [ ] `## In short` with 3 to 5 bullets if the post is over 500 prose words.
- [ ] No sentence over 25 words (35 is the hard limit); section means 20 or below.
- [ ] No sentence with more than 2 code spans; no more than 8 spans per 100 prose words.
- [ ] No identifier used as a verb or bare noun.
- [ ] Parallel items are in a table or list; multi-identifier snippets are in code blocks.
- [ ] A heading at least every ~250 words; no more than 4 prose paragraphs in a row.
- [ ] Invariant check exits 0 (rewrites); the slug is out of the baseline.
