# std::accumulate with a 0 over doubles returns an int, and fold_left does not

## Body
A LinkedIn post by Prince Patel showed three ways to sum an array in PHP. The C++ version has a trap: std::accumulate takes its result type from the initial value. Over three 0.5 values with an initial 0 it returns the int 0, and std::ranges::fold_left returns the double 1.5. GCC 16.2 and Clang 22.1 printed no warning in my runs on 2026-11-17. MSVC and clang-tidy did.

https://wrocpp.github.io/posts/accumulate-zero-truncates-doubles/

## Hashtags
#cpp #cpp26 #algorithms #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Three halves sum to 0 when accumulate starts at 0" with a subtitle about the result type of std::accumulate, fold_left returning 1.5, and which compilers warn. Citation footer: wro.cpp, 2026-12-25.

## Suggested post time
Friday 2026-12-25, 08:00 UTC
Reason: the morning slot on the publication day of the daily post program.
