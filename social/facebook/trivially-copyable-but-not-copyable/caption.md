# Trivially copyable, and not copyable

## Body
On a conforming compiler, all three of these hold for the same type:

  is_trivially_copyable_v<Nutshell>    true
  is_copy_constructible_v<Nutshell>    false
  is_copy_assignable_v<Nutshell>       false

Trivially copyable, and you cannot copy it. From Arthur O'Dwyer's P3279R0.

The mechanism: declaring the move operations suppresses the copies, so no eligible copy operation remains, and the trait's question passes by having nothing left to fail.

MSVC says true, GCC and clang say false, and the paper says MSVC is the one following the standard. I checked and two years on it is unchanged.

Worth correcting one thing: this is not any aggregate holding a non-trivially-copyable member. A plain aggregate is false everywhere, MSVC included.

Three compilers, one file: https://wrocpp.github.io/posts/trivially-copyable-but-not-copyable/

## Hashtags
#cpp #cplusplus #typetraits #programming

## Alt-text
A wro.cpp card about a type-trait divergence between compilers.

## Suggested post time
Thursday 2026-10-22, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
