# std::accumulate with a 0 over doubles returns an int, and fold_left does not

## Body
Prince Patel posted a PHP picture of three ways to sum an array and asked which one you would merge. Here is the C++ version of the question, with one trap in it.

std::accumulate takes its result type from the initial value. Over a vector of three 0.5 values, std::accumulate(v.begin(), v.end(), 0) returns the int 0. A loop and std::ranges::fold_left (C++23) return the double 1.5. The example checks both result types with static_assert.

On Compiler Explorer on 2026-11-17, GCC 16.2 and Clang 22.1 printed no warning, with -Wall -Wextra -Wconversion on GCC and -Weverything on Clang. MSVC warns with C4244 at its default level, and clang-tidy's bugprone-fold-init-type warns too.

For int, the loop, accumulate and fold_left give the same add loop at -O2 on GCC 16.2, and all three vectorise at -O3 on GCC 16.2 and Clang 22.1. std::saturating_add is the C++26 answer to overflow. I would merge fold_left, and accumulate only with an initial value of the element type.

https://wrocpp.github.io/posts/accumulate-zero-truncates-doubles/

## Hashtags
#cpp #cpp23 #cpp26 #algorithms #fold_left #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Three halves sum to 0 when accumulate starts at 0" with a subtitle about the result type of std::accumulate, fold_left returning 1.5, and which compilers warn. Citation footer: wro.cpp, 2026-12-25.

## Suggested post time
Friday 2026-12-25, 08:00 UTC
Reason: the morning slot on the publication day of the daily post program.
