# SIMD in C++ 2026

## Body
Picking a SIMD path in C++26: `std::simd` (P1928) for portable kernels, Google Highway for cross-arch dispatch, ISPC for SPMD-natural workloads, intrinsics for last-cycle tuning. But layout matters more than instruction choice -- every path wants Structure-of-Arrays. Pre-2026 SoA was hand-coded boilerplate; reflection now derives it from struct shape. Demo: ~2.4x speedup AoS -> SoA at -O2, no SIMD intrinsics in user code.

https://wrocpp.github.io/toolset/simd-in-cpp-2026/

## Hashtags
#cpp #cpp26 #simd #performance #reflection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "SIMD in C++ 2026". Subhead: std::simd + Highway + ISPC + reflection-derived SoA. Citation: wro.cpp 2026-06-05.

## Suggested post time
Friday 2026-06-05, 10:00 CET
Reason: Friday morning EU audience.
