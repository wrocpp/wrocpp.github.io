# SIMD in C++ 2026: std::simd, Highway, ISPC, and reflection-derived SoA (~2.4x at -O2)

## Body
SIMD in C++ used to mean "include the right intrinsics header for your microarchitecture and pray the next CPU still has them". C++26 changed the picture twice: **`std::simd` (P1928) ships portable vector types in the standard**, and **reflection makes Structure-of-Arrays a derive-from-shape transform**.

The four paths in 2026:
- **`std::simd`** -- portable, the default starting point; libc++ + libstdc++ both track C++26
- **[Google Highway](https://github.com/google/highway)** -- runtime dispatch across SSE / AVX2 / AVX-512 / NEON / SVE / RVV; used in JPEG XL
- **[ISPC](https://github.com/ispc/ispc)** -- shader-style SPMD when the kernel is naturally that shape (image, DSP, sim)
- **Raw intrinsics** -- last-cycle tuning for instructions the abstractions don't expose

But here's the bigger lever: **layout matters more than instruction choice.** Every SIMD path -- standard, library, compiler-extension, intrinsic -- prefers Structure-of-Arrays. Pre-2026 the SoA transform was hand-coded boilerplate (write a parallel `ParticleSoA`, keep it in sync, regret it on the next member addition). C++26 reflection makes it derive from the struct itself:

```cpp
struct Particle { float x, y, z, vx, vy, vz; };

// Reflection-derived: one std::array<member-type, N> per member,
// indexed accessors via splice + tuple-get.
template <typename T, size_t N> struct SoA;

SoA<Particle, 1024> soa;
for (size_t i = 0; i < 1024; ++i) {
    soa.at<0>(i) += soa.at<3>(i);  // x += vx
    soa.at<1>(i) += soa.at<4>(i);  // y += vy
    soa.at<2>(i) += soa.at<5>(i);  // z += vz
}
```

Measured on aarch64 inside the wro.cpp container: AoS hot loop 479 us, SoA hot loop 199 us -- **~2.4x speedup at -O2 with no SIMD intrinsics in user code**. On x86-64 with AVX2 the gap widens further. Pair the reflection-derived layout with `std::simd` for explicit kernels when you need control beyond what `-march=native` extracts.

The same `nonstatic_data_members_of` walker drives the [hardened-stdlib](https://wrocpp.github.io/toolset/hardened-stdlib/), [qualified-compilers MISRA](https://wrocpp.github.io/toolset/qualified-compilers/), and [lifetime-safety borrow](https://wrocpp.github.io/toolset/lifetime-safety-2026/) lints. One walker, four orthogonal rules. Add a fifth -- "all members arithmetic so SoA can use std::simd directly" -- and you have a strict-SIMD profile that catches structurally non-vectorisable schemas at compile time.

C++29 candidate features collapse the loop further: P3294 token injection lets `[[inject(simd_friendly, soa, step_kernel)]] struct Particle` emit the SoA layout AND the std::simd-driven step() function from one declaration.

https://wrocpp.github.io/toolset/simd-in-cpp-2026/

## Hashtags
#cpp #cpp26 #simd #stdsimd #highway #ispc #performance #reflection #soa #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "SIMD in C++ 2026". Subhead: std::simd / Highway / ISPC + reflection-derived SoA layout (~2.4x at -O2 over AoS, no intrinsics). Citation: wro.cpp 2026-06-05.

## Suggested post time
Friday 2026-06-05, 10:00 CET
Reason: Friday morning EU C++ + game-dev + DSP audience; toolset launch fits the off-day cadence between reflection-series posts.
