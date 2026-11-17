# Value{v} built a one-element array, not a copy, and a check flags those lines

## Body
Episode 3 of a series on clang-tidy checks for AI-written C++. With a std::initializer_list constructor, Value{v} makes an array holding v instead of copying it, on GCC and Clang but not on MSVC. A query check reported 2 of 2 such lines in the example. It misses Value{3} and std::vector<int>{3}.

https://wrocpp.github.io/posts/tidy-agent-brace-init-list-hijack/

## Hashtags
#cpp #clangtidy #initializerlist #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A copy in braces became an array of 1" with a subtitle about a clang-tidy query check that flags 2 of 2 such lines and misses Value{3} and vector<int>{3}. Citation footer: wro.cpp, 2026-12-03.

## Suggested post time
Thursday 2026-12-03, 08:00 UTC
Reason: the morning slot on the publication day; episode 3 of the tidy-agent series, which runs 1 to 9 December.
