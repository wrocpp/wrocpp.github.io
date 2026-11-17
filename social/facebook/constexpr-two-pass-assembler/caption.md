# Two passes in one constexpr function: labels in a compile-time assembler

## Body
A forward jump needs two passes, because its label is not defined yet. Andrew Alekseev solved it by running the program twice. In a constexpr function the two passes are two loops. Mine assembles nine x86-64 instructions into 44 bytes, checks them with a static_assert, and runs them on native x86-64: the program sums 3 + 2 + 1 and returns 6.

https://wrocpp.github.io/posts/constexpr-two-pass-assembler/

## Hashtags
#cpp #constexpr #assembler #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Two passes are two loops in a constexpr function" with a subtitle about a compile-time assembler, 44 bytes of x86-64 and a program that returns 6. Citation footer: wro.cpp, 2026-12-16.

## Suggested post time
Wednesday 2026-12-16, 08:00 UTC
Reason: the morning slot on publication day.
