# Portable SIMD is in C++26, and you can try it now

## Body
Hand-written SIMD means picking a side. Intrinsics are fast and tie you to one instruction set, so a NEON port becomes a second implementation plus an ifdef maze. Plain loops plus hope works until the auto-vectorizer quietly stops cooperating.

C++26 standardises the middle path: <simd>, where the element type and width are part of the type and ordinary arithmetic operators emit vector instructions. One source compiles to SSE, AVX, or NEON with no intrinsics.

GCC 16.1 does not ship the standard header yet, but it ships the experimental version the standard type grew from, and the model is identical. The demo prints width = 4 on the baseline x86-64 target; with -march=x86-64-v3 it becomes 8. Migrating later is mostly a rename.

https://wrocpp.github.io/posts/portable-simd/

## Hashtags
#cpp #cplusplus #cpp26 #simd #performance

## Alt-text
A cream wro.cpp social card reading "SIMD without a single intrinsic", about C++26 portable SIMD.

## Suggested post time
Saturday 2026-09-05, 10:00 CET
Reason: weekend mid-morning for a performance read.
