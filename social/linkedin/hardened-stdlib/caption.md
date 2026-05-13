# Hardened stdlib in 2026: one CMake line, ~1000 production bugs caught

## Body
Most C++ memory-safety bugs that ship in production are not "I wrote a raw memcpy with a hand-rolled offset." They are `vector[i]` where `i` came from an untrusted file, `*ptr` where `ptr` got `reset()` in a sibling thread, `string.front()` on an empty parse result. C++26 ratified the Hardened standard library (P3471 Varlamov + Dionne). Google reports **0.3% perf cost across hundreds of millions of LOC, 1000+ bugs found**. The cost to opt in is one CMake line.

```cmake
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_definitions(_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST)
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    add_compile_options(-fhardened)         # GCC 14+ umbrella
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    add_compile_definitions(_ITERATOR_DEBUG_LEVEL=1)
endif()
```

That catches `vector::operator[]` OOB, deref of null `unique_ptr`/`shared_ptr`/`optional`, `span` access past extent, `string` overruns. What it does NOT catch: raw-pointer arithmetic and C-arrays -- those sit outside the std::* access points the hardened guarantees hook into.

That gap is where C++26 reflection earns its keep. A consteval predicate walks `nonstatic_data_members_of(^^T)` and `static_assert`s that no field is a raw pointer or C-style array. Add a `std::vector` member, the check passes; add an `int*`, the build refuses with the field name in the diagnostic. The hardened stdlib protects you when you USE std::vector; the reflection lint protects you when you DECLARE the schema.

The toolset page lays out the macro per implementation (libc++ FAST/EXTENSIVE/DEBUG, libstdc++ `-fhardened`, MSVC `_ITERATOR_DEBUG_LEVEL`), what each catches at what cost, and the reflection-driven schema lint as the bootstrap that closes the gap until C++29 profiles ship.

https://wrocpp.github.io/toolset/hardened-stdlib/

## Hashtags
#cpp #cpp26 #hardenedstdlib #memorysafety #reflection #p3471 #wrocpp #moderncpp #security

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Hardened stdlib in 2026: one CMake line, ~1000 production bugs caught". Subhead: P3471 ratified in C++26; libc++ FAST mode + libstdc++ -fhardened + MSVC iterator checks; reflection lint closes the schema gap. Citation: wro.cpp 2026-05-24.

## Suggested post time
Sunday 2026-05-24, 10:00 CET
Reason: Sunday morning EU C++ audience; toolset launch fits the off-day cadence between reflection-series posts.
