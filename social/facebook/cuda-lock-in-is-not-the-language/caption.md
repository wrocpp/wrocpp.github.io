# The warp primitive ported fine

## Body
The usual account says CUDA warp primitives weld your source to Nvidia hardware, so porting means rewriting. The first half is accurate and the conclusion is checkable.

I took a warp reduction using __shfl_down_sync and handed it, unmodified, to SCALE, a third-party toolchain that targets AMD. It compiles, and the shuffle comes out as AMD's native cross-lane instructions with the addition fused in. Nvidia's own output needs two separate instructions.

Along the way: PTX and SASS are genuinely different programs, instruction selection changes between sm_80 and sm_90, and CUDA 13.3 refuses Volta outright.

The lock-in is real. It is the toolchain, the headers and the licence, not the language.

This is one half of a joint piece with Neil Talap, whose article covers the history behind the lock-in. Read them together.

Neil's half: https://neiltalap.com/blog/nvidia-and-the-price-of-control

Mine, all reproducible: https://wrocpp.github.io/posts/cuda-lock-in-is-not-the-language/

## Hashtags
#cpp #cplusplus #cuda #gpu #programming

## Alt-text
A wro.cpp card about CUDA portability and lock-in.

## Suggested post time
Saturday 2026-09-26, 18:15 CEST (16:15Z)
Reason: weekday mid-morning CET suits the EU C++ audience.
