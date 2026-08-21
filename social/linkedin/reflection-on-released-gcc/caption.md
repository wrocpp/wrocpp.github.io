# You do not need the fork any more

## Body
If you have read about C++26 reflection, you have probably read that trying it means fetching the Bloomberg clang fork. That was true for a long time and it is not true now.

Daniel Lemire posted a small program that prints values alongside their types. It is a good test case because it uses three C++26 features at once: an expansion statement over a heterogeneous pack, the reflection operator, and range formatting for a vector.

Compile it with g++ -std=c++26 -freflection and it runs. GCC 16.1 has had this since April.

Note the header is <meta>, the standard spelling, not <experimental/meta>. GCC only accepts the former and the fork accepts both, so <meta> is what to write, and writing it makes your code portable across the two.

The two implementations do not agree on everything, though. Same source:

  GCC 16.1     const char*      std::vector<int>
  clang fork   const char *     vector<int, allocator<int>>

GCC qualifies the name and elides the defaulted allocator; the fork does neither. Both are defensible renderings, which is exactly why you should not parse what display_string_of returns. It is for humans reading diagnostics. If you need something stable, identifier_of gives the declared name.

Not everything works. Feeding GCC a range through a named constexpr local rather than inline trips it, which I wrote up separately because the reduced case is short.

Why this matters more than it sounds: "it is in C++26" and "you need a research fork to try it" are different statements, and the second is what stops people looking. GCC 16.2 arrived in August and Fedora 45 has an accepted change to make it the system toolchain.

Runnable on a compiler you already have: https://wrocpp.github.io/posts/reflection-on-released-gcc/

## Hashtags
#cpp #cplusplus #cpp26 #reflection #gcc

## Alt-text
A wro.cpp card reading "You do not need the fork any more", about C++26 reflection on released GCC.

## Suggested post time
Tuesday 2026-10-20, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
