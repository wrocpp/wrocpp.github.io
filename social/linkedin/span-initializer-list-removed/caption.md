# C++26 removes a std::span constructor

## Body
The C++ working draft no longer has the initializer_list constructor of std::span. P2447 added it for C++26, and P4144R1 (LWG issue 4520) takes it out again. In the draft repository the removal is part of the 2026-03 LWG motion, merged on 2026-04-19.

The reason is a line like std::span<const bool> s{ptr, n}. Braces prefer an initializer_list constructor when one is viable, and a pointer and a count both convert to bool, so the line builds a span of two bools instead of a span over n elements. The standard calls that conversion narrowing and ill-formed. GCC 15 compiles it with a warning and s.size() is 2; clang 19 to 22 with libc++ rejects it.

I ran one demo on Compiler Explorer over a three-element array. libstdc++ 15 gives size 2 for span<const bool>, and libstdc++ 16 and libc++ 23.1 give size 3. The span<const int> line gives 3 on every build. libc++ 23 lists P4144R1 among its implemented papers, though its release notes page was still headed In-Progress.

What is not known: the paper links a post by Arthur O'Dwyer about using the constructor in Chromium, and I have not read it. I did not read the plenary minutes either, so "approved in Croydon" rests on the LWG issue note and the draft commit.

https://wrocpp.github.io/posts/span-initializer-list-removed/

## Hashtags
#cpp #cplusplus #cpp26 #stdlib #span #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo and an AI-generated label. Headline reads "C++26 removes a std::span constructor" with a subtitle saying the same braced span line has size 2 on libstdc++ 15 and size 3 on 16. Citation footer: wro.cpp, 2026-10-16.

## Suggested post time
Friday 2026-10-16, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
