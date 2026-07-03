# The unit bug that crashed into Mars

## Body
On September 23, 1999, NASA lost a $327 million spacecraft to a unit conversion. Ground software reported thruster impulse in pound-force seconds; the trajectory code read newton seconds. Every burn was silently wrong by a factor of 4.45 -- for months -- until the Mars Climate Orbiter hit the atmosphere 170 km too low.

No exception. No assertion. The numbers were just numbers.

mp-units makes that entire bug class uncompilable. A value's unit is part of its type: pound-force seconds and newton seconds either convert exactly and explicitly, or the code does not compile. Zero runtime cost -- the dimensional analysis happens entirely at compile time. The demo in the post runs live in your browser on Compiler Explorer.

This kicks off a series, because mp-units is more than "a double with a label": quantity kinds that catch same-dimension bugs (Hz vs Bq), an affine space for points vs deltas, one-line custom units, unit-safe formatting -- and P3045, the proposal to put all of it into C++29.

One more reason we care: the proposal's lead author is Mateusz Pusz of Gdansk, an ISO C++ committee voting member. The strongest bid to give C++ standard physical units is being led from Poland.

Episode 1: https://wrocpp.github.io/posts/unit-bug-mars-orbiter/ -- what unit bug has bitten YOUR codebase?

## Hashtags
#cpp #cplusplus #cpp29 #mpunits #typesafety #safety #wg21

## Alt-text
A cream wro.cpp-branded social card titled "The unit bug that crashed into Mars" with a sub-claim that NASA lost a $327M orbiter to a unit mismatch that mp-units makes uncompilable.

## Suggested post time
Wednesday 2026-07-29, 10:00 CET
Reason: post lands on its own pubDate; Wednesday mid-morning CET catches the EU working-C++ audience.
