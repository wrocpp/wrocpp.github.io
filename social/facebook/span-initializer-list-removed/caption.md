# C++26 removes a std::span constructor

## Body
P4144R1 (LWG issue 4520) removes the initializer_list constructor that C++26 had added to std::span, and the draft dropped it in the 2026-03 LWG motion. The bug was a line like span<const bool> s{ptr, n}, which braces turned into a list of two bools.

On Compiler Explorer the same line gives size 2 on libstdc++ 15 and size 3 on libstdc++ 16 and libc++ 23.1, and clang 19 to 22 rejects it.

I did not read the Chromium post that the paper links, so how the feature might return is open.

https://wrocpp.github.io/posts/span-initializer-list-removed/

## Hashtags
#cpp #cplusplus #cpp26 #stdlib #span #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo and an AI-generated label. Headline reads "C++26 removes a std::span constructor" with a subtitle about the same braced span line having size 2 on libstdc++ 15 and size 3 on 16. Citation footer: wro.cpp, 2026-10-16.

## Suggested post time
Friday 2026-10-16, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
