# Keeping the early exit and getting vector code on a 64-byte compare

## Body
The previous post showed a 64-byte compare with an early exit staying scalar. This one keeps the early exit and still gets vector code.

Cut the loop into chunks of 16 or 32 bytes, test each chunk at once, and exit only between chunks. With 32-byte chunks and -O3 -march=x86-64-v3, GCC 16.2 emits 12 instructions and Clang 23.1 emits 13. At -O2 the chunked forms take 23 to 47 instructions, more than the scalar loop, and 8-byte chunks do worse.

std::simd in GCC 16.2 compiles the same compare to 10 instructions at v3. These are instruction counts from Compiler Explorer. I did no timing, so measure before you choose.

https://wrocpp.github.io/posts/early-exit-loop-vectorization/

## Hashtags
#cpp #compilers #vectorization #simd #gcc #clang #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Chunks keep the early exit and vectorize" with a subtitle about instruction counts on GCC and Clang. Citation footer: wro.cpp, 2026-11-29.

## Suggested post time
Sunday 2026-11-29, 16:00 UTC
Reason: the second slot of the day, beside the annotations post.
