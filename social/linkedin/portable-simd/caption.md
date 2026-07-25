# Portable SIMD is in C++26, and you can try it now

## Body
Writing SIMD by hand means picking a side. Intrinsics like _mm256_add_ps are precise and fast and tie the code to one instruction set, so a NEON port becomes a parallel implementation plus an ifdef maze. The alternative, plain loops plus hope, works until the auto-vectorizer silently stops cooperating, usually because of a pointer alias it cannot rule out.

C++26 standardises the middle path: <simd>, where the element type and the width are part of the type and ordinary arithmetic operators do the work.

  std::simd<float> a = 1.5f;
  std::simd<float> b = 2.0f;
  auto c = a * b;      // one instruction, whatever the target supports

The library picks a native width, so the same source compiles to SSE, AVX-512, or NEON. No intrinsics, no per-architecture ifdef, and the vectorization is explicit rather than a hopeful side effect of -O3.

GCC 16.1 does not ship the standard header yet, but it ships the Parallelism TS version the standard type grew out of, which is the same programming model. The demo prints width = 4 on Compiler Explorer's baseline x86-64 target; compile with -march=x86-64-v3 and it becomes 8, on ARM it becomes NEON. Migrating later is mostly a rename.

It is for data-parallel arithmetic you already know vectorizes in principle: pixel and audio buffers, physics steps, distance kernels. It will not rescue code whose real problem is memory bandwidth or a dependency chain.

https://wrocpp.github.io/posts/portable-simd/

Have you shipped intrinsics you would rather have written once?

## Hashtags
#cpp #cplusplus #cpp26 #simd #performance #hpc

## Alt-text
A cream wro.cpp social card reading "SIMD without a single intrinsic", about C++26 portable SIMD.

## Suggested post time
Saturday 2026-09-05, 10:00 CET
Reason: weekend mid-morning for a longer performance read.
