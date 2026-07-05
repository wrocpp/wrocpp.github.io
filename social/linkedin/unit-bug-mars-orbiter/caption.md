# The unit bug that crashed into Mars

## Body
On September 23, 1999, NASA lost a $327 million spacecraft to a unit conversion. Ground software reported thruster impulse in pound-force seconds; the trajectory code read newton seconds. Every burn was silently wrong by a factor of 4.45, for months, until the Mars Climate Orbiter hit the atmosphere 170 km too low. Nothing threw and nothing asserted. The numbers were just numbers.

mp-units makes that entire bug class uncompilable. A value's unit is part of its type, so pound-force seconds and newton seconds either convert exactly and explicitly or the code does not compile. The dimensional analysis happens at compile time, so there is no runtime cost. The demo in the post compiles and runs on Compiler Explorer.

This kicks off a series, because mp-units does more than attach a label to a double. It has quantity kinds that catch same-dimension bugs (Hz vs Bq), an affine space for points versus deltas, one-line custom units, and unit-safe formatting. All of it is on the C++29 standard track as P3045.

The proposal's lead author is Mateusz Pusz of Gdansk, an ISO C++ committee voting member.

Episode 1: https://wrocpp.github.io/posts/unit-bug-mars-orbiter/

What unit bug has bitten your codebase?

## Hashtags
#cpp #cplusplus #cpp29 #mpunits #typesafety #safety #wg21

## Alt-text
A cream wro.cpp-branded social card titled "The unit bug that crashed into Mars" with a sub-claim that NASA lost a $327M orbiter to a unit mismatch that mp-units makes uncompilable.

## Suggested post time
Wednesday 2026-07-29, 10:00 CET
Reason: post lands on its own pubDate; Wednesday mid-morning CET catches the EU working-C++ audience.
