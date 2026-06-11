# C++26 Contracts: four enforcement modes, one migration path

## Body
Contracts shipped in C++26 after a contested 114-12-3 vote. P2900 adds pre(), post(), and contract_assert(), each with four evaluation modes you pick at compile time: ignore, observe, enforce, quick_enforce. GCC 16.1 implements all four via -fcontracts.

The practical win is the migration path: run observe in staging to log violations without crashing, triage, then flip to enforce in production. Contracts even double as a fuzzing oracle -- the predicate is the test.

Our toolset page walks the syntax, the replaceable handler, and the observe-to-enforce path.

https://wrocpp.github.io/toolset/contracts-2026/

## Hashtags
#cpp #cpp26 #contracts #safety #gcc

## Alt-text
Dark wro.cpp card. Headline "Four enforcement modes, one migration path" with the line "P2900 shipped in C++26 with four evaluation semantics, on GCC 16.1."

## Suggested post time
2026-07-03, 10:00 CET
