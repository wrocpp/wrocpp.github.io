# Keeping the early exit and getting vector code on a 64-byte compare

## Body
Split a 64-byte compare into chunks of 16 or 32 bytes that exit between chunks, and GCC and Clang compile each chunk to a vector test. With 32-byte chunks and AVX2 flags that is 12 instructions on GCC and 13 on Clang. At -O2 the chunked forms are longer than the scalar loop, and I did no timing.

https://wrocpp.github.io/posts/early-exit-loop-vectorization/

## Hashtags
#cpp #compilers #vectorization #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Chunks keep the early exit and vectorize" with a subtitle about instruction counts on GCC and Clang. Citation footer: wro.cpp, 2026-11-29.

## Suggested post time
Sunday 2026-11-29, 16:00 UTC
Reason: the second slot of the day, beside the annotations post.
