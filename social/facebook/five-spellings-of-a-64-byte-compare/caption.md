# Five ways to compare 64 bytes, and what GCC, Clang and MSVC make of them

## Body
Compare 64 bytes with a loop that returns at the first difference, and Clang and MSVC keep it scalar in every build I made. GCC vectorizes it only with AVX2 flags. Array equality, memcmp and std::equal gave the same instructions as each other in all ten builds.

https://wrocpp.github.io/posts/five-spellings-of-a-64-byte-compare/

## Hashtags
#cpp #compilers #vectorization #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A 64-byte compare loop stays scalar on Clang and MSVC" with a subtitle about the library spellings compiling to the same instructions. Citation footer: wro.cpp, 2026-11-25.

## Suggested post time
Wednesday 2026-11-25, 16:00 UTC
Reason: the second slot of the day, beside the co_yield post.
