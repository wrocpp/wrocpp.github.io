# Hardened stdlib in 2026

## Body
C++26 ratified the Hardened standard library (P3471). Google ran it across hundreds of millions of LOC: **0.3% perf cost, 1000+ bugs caught**. Opt-in is one CMake line per implementation -- libc++ FAST mode, libstdc++ `-fhardened`, MSVC iterator checks.

What it catches: `vector::operator[]` OOB, null smart-pointer deref, `span` over-read, `string` overruns. What it does NOT catch: raw pointers and C-arrays. The toolset page closes that gap with a reflection-driven schema lint -- `static_assert` refuses to compile structs that have `int*` or `char[N]` members.

https://wrocpp.github.io/toolset/hardened-stdlib/

## Hashtags
#cpp #cpp26 #hardenedstdlib #memorysafety #reflection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Hardened stdlib in 2026". Subhead: P3471 in C++26; one CMake line; reflection closes the schema gap. Citation: wro.cpp 2026-05-24.

## Suggested post time
Sunday 2026-05-24, 10:00 CET
Reason: Sunday EU C++ audience; toolset launch fills off-day cadence.
