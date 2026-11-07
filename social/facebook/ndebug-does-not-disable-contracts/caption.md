# -DNDEBUG does not turn off contract_assert on GCC 16.2

## Body
On GCC 16.2, -DNDEBUG deletes the assert macro and leaves contract_assert running. With -fcontracts, a false contract terminates the program even with -O3 -flto.

Only -fcontract-evaluation-semantic=ignore stopped the evaluation. A release build that relied on NDEBUG to remove every check keeps its contract checks.

https://wrocpp.github.io/posts/ndebug-does-not-disable-contracts/

## Hashtags
#cpp #cpp26 #contracts #gcc #releasebuilds #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "NDEBUG leaves contract checks running on GCC 16.2" with a subtitle about -fcontracts and the evaluation semantic. Citation footer: wro.cpp, 2026-11-16.

## Suggested post time
Monday 2026-11-16, 08:00 UTC
Reason: a single post that day, so the morning slot.
