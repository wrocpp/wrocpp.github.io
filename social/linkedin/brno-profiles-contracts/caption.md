# Safety profiles arrive, virtual contracts return

## Body
The other half of Brno's safety story was the concrete one: profiles and contracts. Both opt you in to more checking than baseline C++ gives you, and both moved at the meeting. All of it targets C++29.

P3589R2, "C++ Profiles: The Framework" (Dos Reis), supplies the plumbing, and the key detail is that it is built from attributes, not pragmas. [[profiles::enforce(...)]] turns a profile on for a translation unit; [[profiles::suppress(...)]] is the local escape hatch, scoped to a statement and forced to carry a justification string. Enforcement is broad, suppression is narrow and loud -- on purpose. Stroustrup brought two concrete profiles on that framework: P4222, an initialization profile (no reading uninitialized objects), and P3984, a type-safety profile composed from casting, union, ranges, and arithmetic sub-profiles.

And the cleanest adoption for contract watchers: P3097, "Contracts for C++: Virtual functions" (Doumler, Berne). Cut from the C++26 MVP at Hagenberg, it returns -- with no implicit inheritance of assertions. On a virtual call, both the static function's and the final overrider's contracts are evaluated. It ships with a complete GCC implementation.

https://wrocpp.github.io/posts/brno-profiles-contracts/

## Hashtags
#cpp #cpp29 #wg21 #safety #profiles #contracts #moderncpp #wrocpp

## Alt-text
Editorial card with headline "Safety profiles arrive, virtual contracts return" and subtitle "Brno's C++29 safety track: an enforce attribute for profiles, contracts on overrides."

## Suggested post time
2026-06-19, 10:00 CET
