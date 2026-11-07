# Five ways to compare 64 bytes, and what GCC, Clang and MSVC make of them

## Body
A loop that compares 64 bytes and returns at the first difference stays scalar on Clang and MSVC in every build I made. GCC vectorizes it only with AVX2 flags, and then behind alignment checks.

The loop comes from u/Sopel97's thread on r/cpp. I rebuilt it as five spellings and compiled them on GCC 16.2 and a 17 snapshot, Clang trunk and 23.1, and MSVC 19.51. Array equality, memcmp and std::equal produced the same instructions as each other in all ten builds. The same loop returning int instead of bool vectorizes on Clang.

The post quotes the compiler messages that explain each result, and it ends with a list of what I did not run. These are instruction counts from Compiler Explorer, not timings.

https://wrocpp.github.io/posts/five-spellings-of-a-64-byte-compare/

## Hashtags
#cpp #compilers #vectorization #gcc #clang #msvc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A 64-byte compare loop stays scalar on Clang and MSVC" with a subtitle about the library spellings compiling to the same instructions. Citation footer: wro.cpp, 2026-11-25.

## Suggested post time
Wednesday 2026-11-25, 16:00 UTC
Reason: the second slot of the day, beside the co_yield post.
