# reflect_soa: AoS / SoA / AoSoA from one struct + an A/B harness that picks for you (capstone post 25)

## Body
Data-oriented design has been telling C++ "AoS is bad" for twenty years. The reason it stayed rare: writing SoA by hand is painful and splits your logical model from your memory layout. C++26 reflection collapses that. Capstone of the wro.cpp 25-post arc:

```cpp
struct Particle { float x, y, z, vx, vy, vz; };

reflect_soa::SoaVector<Particle> particles(100'000);
for (auto& p : particles) {
    p.x += p.vx;       // appears as struct access; backed by SoA columns
    p.y += p.vy;
    p.z += p.vz;
}
// Internally: 6 separate std::vector<float> columns, stride-1 access,
// auto-vectoriser sees fused-multiply-add hot loop, NEON / AVX2 lights up.
```

Three layouts derive from the same struct:
- **AoS** (Array-of-Structures): the hand-written default; classic cache miss on partial-field iteration
- **SoA** (Structure-of-Arrays): one column per member, stride-1 SIMD-friendly access
- **AoSoA** (Array-of-Structures-of-Arrays): cache-line-aligned blocks, best of both worlds for mixed-access workloads

And an **A/B benchmark harness**: `reflect_soa::pick<Particle>(workload)` runs the workload three ways and tells you which layout wins. Workload-dependent; benchmarking is the only honest answer.

Prior art: Barry Revzin's 2025 blog post "Implementing a Struct of Arrays" showed the SoA-via-reflection pattern; reflect_soa productises it and adds AoSoA + the A/B harness. Cross-link: the [simd-in-cpp-2026 toolset entry](https://wrocpp.github.io/toolset/simd-in-cpp-2026/) covers std::simd / Highway / ISPC. Pair with reflect_soa for the layout transform that unlocks them.

What this REPLACES: the parallel `ParticleSoA` struct you write by hand; the discipline of keeping it in sync with `Particle`; the regression where someone added `mass` to Particle but forgot to add a column to the SoA mirror; the test you wrote to catch that regression.

What this does NOT replace: domain-specific layout choices (a `Mesh` with vertex / index / texture-coord arrays already has its own layout; `reflect_soa` is for the case where the struct IS the unit of iteration). Profile your code. The A/B harness is the answer to "which layout".

Series post 25 of 25 in the wro.cpp C++26 reflection arc. The arc closes on the data-oriented thesis Mike Acton was right about all along; reflection just made it ergonomic. Live demo on Godbolt with clang-p2996.

https://wrocpp.github.io/posts/reflect-soa/

## Hashtags
#cpp #cpp26 #reflection #performance #soa #aos #aosoa #data-oriented #simd #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_soa". Subhead: AoS / SoA / AoSoA from one struct + A/B benchmark harness. Capstone of the 25-post wro.cpp reflection arc. Citation: wro.cpp 2026-06-29.

## Suggested post time
Monday 2026-06-29, 10:00 CET
Reason: Monday morning EU C++ + data-oriented-design audience; capstone post deserves the Monday slot. Closes the every-2-day reflection arc.
