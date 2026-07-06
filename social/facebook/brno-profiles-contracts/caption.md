# Safety profiles arrive, virtual contracts return

## Body
The concrete half of Brno's safety story: profiles and contracts, both targeting C++29. P3589R2 (Dos Reis) gives profiles a framework built from attributes, not pragmas. [[profiles::enforce(...)]] turns one on for a translation unit, [[profiles::suppress(...)]] is a narrow, justification-carrying escape hatch. Stroustrup brought two profiles on it: an initialization profile (P4222) and a type-safety profile (P3984). And P3097 returns virtual-function contracts that were cut from the C++26 MVP, with no implicit inheritance. Both the static function's and the final overrider's contracts are evaluated, shipping with a complete GCC implementation.

https://wrocpp.github.io/posts/brno-profiles-contracts/

## Hashtags
#cpp #cpp29 #wg21 #safety #profiles #contracts #moderncpp #wrocpp

## Alt-text
Editorial card with headline "Safety profiles arrive, virtual contracts return" and subtitle "Brno's C++29 safety track: an enforce attribute for profiles, contracts on overrides."

## Suggested post time
2026-06-19, 10:00 CET
