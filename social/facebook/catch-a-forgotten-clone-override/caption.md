# Three ways to catch a forgotten clone() override, and where each one stops

## Body
Episode 3 of a series on clone() and smart pointers. A class that forgets its clone hooks can be caught three ways on GCC 16.2: a contract_assert at run time, a static_assert over a constant-evaluated round trip, and a reflection lint. The contract disappears under the ignore semantic, the static_assert covers only listed classes, and the lint sees one namespace. No net covers everything.

https://wrocpp.github.io/posts/catch-a-forgotten-clone-override/

## Hashtags
#cpp #cpp26 #contracts #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Three checks for a forgotten override, each with a limit" with a subtitle naming a contract_assert, a constant-evaluated test and a reflection lint. Citation footer: wro.cpp, 2026-12-19.

## Suggested post time
Saturday 2026-12-19, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
