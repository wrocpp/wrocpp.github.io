# The hidden cost of <meta>: the three-line fix

## Body
Vittorio Romeo measured what C++26 reflection actually costs. The headline: the `<meta>` header adds ~181ms per translation unit on GCC 16.1. The reflection algorithm itself? ~0.07ms per enumerator.

The header is 2500x more expensive than the logic.

The fix is three lines of CMake:

```cmake
target_precompile_headers(my_target PRIVATE
  <meta>
  <ranges>
)
```

PCH cuts the cost by 2.3x. Modules? Surprisingly worse on GCC 16.1 (2.2x slowdown). That will improve in GCC 17, but today PCH is the right answer.

Every project using C++26 reflection should add this to their CMakeLists.txt.

https://wrocpp.github.io/posts/reflection-compile-time-cost/

## Hashtags
#cpp #cpp26 #reflection #p2996 #compiletime #pch #gcc #moderncpp #wrocpp

## Alt-text
Editorial card with the wro.cpp magnet wordmark. Headline: "The hidden cost of <meta>: the three-line fix". Subhead: reflection header costs ~181ms per TU; PCH cuts it by 2.3x; modules are slower on GCC 16.1. Citation: wro.cpp 2026-05-29.

## Suggested post time
Thursday 2026-05-29, 10:00 CET
Reason: Midweek C++ audience; practical content pairs well with the reflection series.
