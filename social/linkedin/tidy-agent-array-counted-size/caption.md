# A std::array with four names for five slots compiles, and the last name is empty

## Body
Episode 1 of a series on clang-tidy checks for mistakes that AI coding agents keep making.

A table declared as std::array<std::string_view, 5> with four names compiles on GCC 16.2 and clang trunk, with no warning from either. The fifth name is an empty string. A list with six names is an error, so the compiler guards only one direction. I tried -Wall -Wextra -Wpedantic on GCC and -Weverything on clang, and none of them reported the short list.

A query check of eight lines in clang-tidy flags the declaration. It ran on clang-tidy trunk on Compiler Explorer and on a local clang-tidy 23.1.5. std::to_array deduces the size, and a static_assert against the enum count states how many entries are wanted.

The limits: the check also flags two cases its own spec says to skip (a size from a named constant, a size from a template parameter), and it does not see a table returned by a function. The plugin twin with a fix-it is not written yet, so I fixed the example by hand.

The post also makes the case for spending tokens on deterministic checks instead of prose rules, with the counter-evidence from Google's migration paper, and lays out the ladder from an existing check to a plugin.

https://wrocpp.github.io/posts/tidy-agent-array-counted-size/

## Hashtags
#cpp #clangtidy #aiagents #stdarray #staticanalysis #cpp20 #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "std::array takes a short list and fills in zeros" with a subtitle about four names for five slots, no compiler warning, a clang-tidy query check and std::to_array. Citation footer: wro.cpp, 2026-12-01.

## Suggested post time
Tuesday 2026-12-01, 08:00 UTC
Reason: the morning slot on the publication day; first episode of nine, 1 to 9 December.
