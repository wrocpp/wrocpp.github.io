# The magic-numbers check reports 103 bare numbers in a test suite, and 19 deserve a name

## Body
Episode 5 of the tidy-agent series. A query check for bare numbers in test comparisons, run on the 43 test files of cloudevents-sdk-cpp, reports 103 unique locations. Reading each line, I found 19 that need a name. The other 84 are sizes, indices, fixture values, pinned constants and loop bounds. The check also matches loop conditions that its spec does not intend, and it cannot see floating literals.

https://wrocpp.github.io/posts/tidy-agent-magic-numbers-in-tests/

## Hashtags
#cpp #clangtidy #aiagents #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "103 hits in one test suite, 19 worth a name" with a subtitle about a query check for bare numbers run on the 43 test files of cloudevents-sdk-cpp. Citation footer: wro.cpp, 2026-12-05.

## Suggested post time
Saturday 2026-12-05, 08:00 UTC
Reason: the morning slot on the publication day; episode 5 of 9 in the tidy-agent series.
