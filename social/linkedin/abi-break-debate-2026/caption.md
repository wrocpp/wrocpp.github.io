# Could C++ handle an ABI break? The 2026 case

## Body
Two pieces dropped in the same week. Luis Caro Campos at CppCon 2025: "Could C++ Developers Handle an ABI Break Today?" -- argues package managers can tag binaries on ABI version, the pain is overestimated. HFT University: "The C++ Standard Library Has Been Walking Itself Back for Fifteen Years" -- documents the unfixable ABI-locked stdlib mistakes, claims tier-one firms (HFT, browsers) already build on Abseil/Folly/EASTL.

The committee position: no break, stability above all. The reason isn't naivety; it's the long tail (embedded, automotive, enterprise) that can't rebuild its dependency tree on a flag day.

Honest take inside.

https://wrocpp.github.io/posts/abi-break-debate-2026/

## Hashtags
#cpp #cpp26 #abi #stdlib #performance #abseil #folly #conan #vcpkg #wrocpp

## Alt-text
Editorial card: "Could C++ handle an ABI break? The 2026 case". The HFT case for breaking + Caro Campos' package manager argument + the committee's stability position.

## Suggested post time
Wednesday 2026-06-10, 10:00 CET
