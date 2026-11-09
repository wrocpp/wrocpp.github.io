# Three ways to catch a forgotten clone() override, and where each one stops

## Body
Episode 3 of a series on clone() and smart pointers.

Three checks catch a class that forgets its clone hooks on GCC 16.2, and each one stops somewhere.

A contract_assert before the cast aborts under the enforce semantic. Under observe it reports and the program goes on, and under ignore nothing is checked. It cannot sit on the hooks, because GCC 16.2 rejects contracts on virtual functions.

A constant-evaluated round trip reports the forgetful class at build time on GCC 16.2 and Clang 22.1, but only for the classes someone listed.

A reflection lint lists every concrete class in a namespace that lacks the overrides, and generated tests clone each one. GCC 16.2 and clang-p2996 print the same output. It sees one namespace of one translation unit.

No net covers everything, and the post sets the limits side by side.

https://wrocpp.github.io/posts/catch-a-forgotten-clone-override/

## Hashtags
#cpp #cpp26 #contracts #reflection #constexpr #undefinedbehavior #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Three checks for a forgotten override, each with a limit" with a subtitle naming a contract_assert, a constant-evaluated test and a reflection lint. Citation footer: wro.cpp, 2026-12-19.

## Suggested post time
Saturday 2026-12-19, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
