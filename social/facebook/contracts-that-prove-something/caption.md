# What a C++ contract would have to be to prove something

## Body
A reader wished for C++ contracts that prove things instead of acting as assertions. I ran each wish on GCC 16.2.

One bad port, reported by four functions in a chain, because a postcondition stays inside its own function. A Port type that checks once cut that to none. A bad constant port is already a compile error, and a check folds away only when the compiler can see the predicate.

https://wrocpp.github.io/posts/contracts-that-prove-something/

## Hashtags
#cpp #cpp26 #contracts #correctness #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One bad port, reported four times" with a subtitle about running a reader's contracts wishlist on GCC 16.2. Citation footer: wro.cpp, 2026-10-27.

## Suggested post time
Tuesday 2026-10-27, 16:00 UTC
Reason: second post of the day, beside the Abseil iterator post at 08:00 UTC.
