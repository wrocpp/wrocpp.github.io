# C++26 Contracts: four enforcement modes, one migration path

## Body
Contracts are the most contested feature in C++26. The vote was 114-12-3. Stroustrup opposed the design. The committee shipped it anyway -- because the alternative was three more years of waiting while the safety pressure mounted.

What landed is useful. P2900 adds pre(), post(), and contract_assert(), each with four evaluation semantics chosen per translation unit at compile time:
- ignore: zero cost, predicate still type-checked
- observe: evaluate, call the handler, keep running (gather violations in staging)
- enforce: evaluate, call the handler, then terminate (production safety net)
- quick_enforce: trap immediately, no handler (hard real-time)

GCC 16.1 implements all four via -fcontracts. The violation handler is replaceable. The real value is the migration path: run observe in staging to collect violations without crashing, triage, then flip to enforce in production. Contracts also double as a fuzzing oracle -- the predicate IS the test.

Our toolset page covers the syntax, the handler, module-boundary and serialization patterns, and the observe-to-enforce migration in detail.

https://wrocpp.github.io/toolset/contracts-2026/

## Hashtags
#cpp #cpp26 #contracts #p2900 #safety #gcc

## Alt-text
Dark wro.cpp card. Headline "Four enforcement modes, one migration path" with the line "P2900 shipped in C++26 with four evaluation semantics, on GCC 16.1."

## Suggested post time
2026-07-03, 10:00 CET
Reason: matches the 08:00 UTC publish slot.
