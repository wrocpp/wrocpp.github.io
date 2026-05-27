# C++ modules in 2026: import std works, your IDE can't

## Body
C++20 modules shipped six years ago. The compilers support them. The ecosystem does not.

import std compiles on GCC 16.1, Clang 18+, and MSVC. Boost has a per-library module prototype showing 45% build-time reductions. But CMake import std is still experimental (gated behind a GUID that changes between releases), clangd needs a full rebuild on module changes, and VS 2026 IntelliSense has been "experimental" for seven years.

For reflection users specifically: Vittorio Romeo's benchmarks show modules are 2.2x slower than plain includes on GCC 16.1 for <meta>. PCH cuts the cost by 2.3x. Use PCH today; watch modules for tomorrow.

https://wrocpp.github.io/posts/modules-2026/

## Hashtags
#cpp #cpp26 #modules #importstd #boost #cmake #pch #reflection #wrocpp

## Alt-text
Editorial card: "C++ modules in 2026: import std works, your IDE can't". Status of module support across compilers, build systems, and IDEs.

## Suggested post time
Friday 2026-06-06, 10:00 CET
