# A std::array with four names for five slots compiles, and the last name is empty

## Body
Episode 1 of a series on clang-tidy checks for mistakes that AI coding agents keep making. A const std::array<T, N> accepts a list shorter than N and fills the tail with zeros. GCC 16.2 and clang trunk gave no warning in my runs. A clang-tidy query check flags the declaration, and std::to_array removes the count. The check also flags two cases its spec says to skip.

https://wrocpp.github.io/posts/tidy-agent-array-counted-size/

## Hashtags
#cpp #clangtidy #aiagents #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "std::array takes a short list and fills in zeros" with a subtitle about four names for five slots, no compiler warning, a clang-tidy query check and std::to_array. Citation footer: wro.cpp, 2026-12-01.

## Suggested post time
Tuesday 2026-12-01, 08:00 UTC
Reason: the morning slot on the publication day; first episode of nine, 1 to 9 December.
