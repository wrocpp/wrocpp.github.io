# WG21 now says new library types must ship a pmr alias

## Body
A recurring worry about std::pmr is that it was a C++17 experiment the committee moved on from. The opposite is happening.

In 2024 WG21 adopted P3002, a policy that new memory-allocating standard types should be allocator-aware, default to std::allocator, and ship a std::pmr alias backed by polymorphic_allocator. Every future allocating container arrives with a pmr form built in, the way pmr::vector and pmr::string already do.

Two papers follow from it. P3153 makes optional allocator-aware, pulling pmr into a core vocabulary type. P1083, targeting C++26, standardizes resource_adaptor: a wrapper that turns any classic C++ allocator into a memory_resource, so the compile-time and runtime allocator models can meet. The demo hand-rolls that bridge in a few lines and drives a pmr::vector from a classic allocator.

The maintenance trail says the same thing. LWG 2969, 3037, and a run of alignment and size fixes have kept pmr in good repair for years. Abandoned features do not get that attention.

pmr is not the whole allocator story. The compile-time model still exists for zero-overhead cases. What pmr offers is the runtime half, and the standard is being built to lean on it. Eight episodes in, the through-line is one small interface, chosen at runtime, that the rest of the library is quietly learning to honor.

Episode 8 of the pmr series.

https://wrocpp.github.io/posts/pmr-future/

## Hashtags
#cpp #cplusplus #cpp26 #pmr #wg21 #memory #moderncpp

## Alt-text
A cream wro.cpp card reading "pmr isn't dead, it's becoming the default", on WG21's pmr direction.

## Suggested post time
Wednesday 2026-10-28, 10:00 CET
Reason: midweek morning CET; closes the series.
