# The hidden cost of <meta>: the three-line fix

## Body
C++26 reflection's `<meta>` header costs ~181ms per translation unit. The reflection algorithm itself? ~0.07ms per enumerator. The header is 2500x more expensive than the logic.

Three lines of CMake (precompiled header) cut the cost by 2.3x. Every project using reflection should add this.

https://wrocpp.github.io/posts/reflection-compile-time-cost/

## Hashtags
#cpp #cpp26 #reflection #compiletime #moderncpp #wrocpp

## Alt-text
Editorial card: "The hidden cost of <meta>: the three-line fix". Reflection header costs ~181ms; PCH cuts by 2.3x.

## Suggested post time
Thursday 2026-05-29, 10:00 CET
