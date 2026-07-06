# After C++26, WG21 turns to undefined behavior

## Body
C++26 is done: reflection, contracts, a hardened standard library, import std. So WG21 met in Brno, Czechia (June 8-13, 2026), the first meeting since C++26 was finalized, and the theme was unmistakable: this was the opening move of C++29, the safety release.

Per Herb Sutter's trip report, the structural move was P3596R3, two new annexes that catalogue every case of undefined behavior and every ill-formed-no-diagnostic-required corner in the standard. Its companion, P3100, turns that catalogue into a case-by-case program of summer and fall telecons to close each one, targeting C++29. Profiles kept marching too (an initialization profile and a type-safety profile from Stroustrup, on the framework from Dos Reis), and contracts grew a feature back: P3097R3 returns virtual-function contracts that were cut from the C++26 MVP.

Reflection? Not on the marquee, and that is exactly what shipping looks like. Once a feature lands, the committee's attention moves on, here to safety.

Three companion posts go deeper this week.

https://wrocpp.github.io/posts/brno-2026-trip-report/

## Hashtags
#cpp #cpp29 #wg21 #moderncpp #safety #undefinedbehavior #contracts #wrocpp

## Alt-text
Editorial card with headline "After C++26, WG21 turns to undefined behavior" and subtitle "The Brno meeting opened C++29 with a UB catalogue, safety profiles, and contracts."

## Suggested post time
2026-06-16, 10:00 CET
