# What a C++ contract would have to be to prove something

## Body
Pavel Simerda wrote that they don't buy contracts as glorified assertions, and listed what would interest them: a postcondition that counts as a promise, a precondition satisfied by the function that produced the argument, and results the compiler knows are 0 or -1.

I ran each wish on GCC 16.2. A postcondition does not reach the caller, so the checks run inside each function and one bad port is reported four times down a call chain. A condition with no body links only when contracts are ignored. When the predicate is visible and the port is a constant, enforce folds every check away and the code equals the ignored build. A bad constant port is already a compile error.

A Port type that checks once at the boundary cut the four reports to none. The post also lists what SPARK, Frama-C, Dafny, Liquid Haskell, Eiffel and Kani check, from their own documentation. GCC only, one version, and I did not ask the author to review it.

https://wrocpp.github.io/posts/contracts-that-prove-something/

## Hashtags
#cpp #cpp26 #contracts #correctness #verification #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One bad port, reported four times" with a subtitle saying a reader's contracts wishlist was run on GCC 16.2: a postcondition stays in its function, a bad constant port is a compile error, and one check in a type cuts four reports to none. Citation footer: wro.cpp, 2026-10-27.

## Suggested post time
Tuesday 2026-10-27, 16:00 UTC
Reason: second post of the day, beside the Abseil iterator post at 08:00 UTC.
