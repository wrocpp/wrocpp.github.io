# Value{v} built a one-element array, not a copy, and a check flags those lines

## Body
Episode 3 of a series on clang-tidy checks for the mistakes AI coding agents keep making.

std::vector<int>{5} has 1 element and std::vector<int>(5) has 5. The same rule applies to a JSON-like Value with a std::initializer_list constructor: Value{v} and return {v}; build a one-element array that holds v, and no copy of v. On GCC 12.1 to 16.2 and Clang 22.1 the example prints "braces: array of 1". MSVC 19.40, 19.44 and 19.51 print "object of 0", so they copy.

The check, wrocpp-brace-init-list-hijack, is a query check. It flags a one-element braced list of the class itself. It reported 2 of 2 lines in the first example and 5 of 8 braced initializations in the second, on clang-tidy trunk (LLVM 24.0.0git) on Compiler Explorer.

What it misses: Value{3} and std::vector<int>{3}, because the element is an int. A deliberate one-element array is flagged too. The spec asks for a fix-it plugin twin that rewrites {x} to (x), and the repository does not have it yet, so I ran no fix-it. The post also reads four cloudevents-sdk-cpp commits where this changed a JSON value into an array. I did not measure how often an agent writes the braced form.

https://wrocpp.github.io/posts/tidy-agent-brace-init-list-hijack/

## Hashtags
#cpp #clangtidy #aicoding #initializerlist #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A copy in braces became an array of 1" with a subtitle about a clang-tidy query check that flags 2 of 2 such lines and misses Value{3} and vector<int>{3}. Citation footer: wro.cpp, 2026-12-03.

## Suggested post time
Thursday 2026-12-03, 08:00 UTC
Reason: the morning slot on the publication day; episode 3 of the tidy-agent series, which runs 1 to 9 December.
