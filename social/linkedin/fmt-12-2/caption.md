# {fmt} can do the whole format at compile time

## Body
std::format checks your format string at compile time, which is the improvement everyone remembers from C++20. What it still does at runtime is parse it: walk the string, find the replacement fields, dispatch on each specifier.

{fmt}, the library std::format came from, can do that work during compilation too. Wrap the format string in FMT_COMPILE and the parse happens once, at compile time, emitting straight-line formatting code instead of a parse loop. The function in the demo is constexpr and returns a fully formatted string. Width, zero-fill and field order are all resolved during compilation.

On a hot path that formats with a fixed layout, log lines, wire protocols, filenames, that removes the parse from every call. It is not free in every dimension, since specialised code is emitted per call site, so it is a targeted tool rather than a default.

The 12.2 release adds three things worth knowing: a type-safe C formatting API, which is an unusual direction for a C++ library and aimed at C code that wants printf ergonomics with type safety; a dedicated C++20 module target so import fmt is a supported configuration; and the full Dragonbox cache enabled by default, which speeds up float formatting at a modest cost in binary size.

Why keep using {fmt} when std::format exists? It is where features arrive first and where the ones that never made the standard live. There is no standard equivalent of FMT_COMPILE.

Runs live on Compiler Explorer: https://wrocpp.github.io/posts/fmt-12-2/

## Hashtags
#cpp #cplusplus #fmt #formatting #performance #programming

## Alt-text
A cream wro.cpp social card reading "A format call that costs nothing at runtime", about FMT_COMPILE and fmt 12.2.

## Suggested post time
Wednesday 2026-08-12, 10:00 CET
Reason: midweek mid-morning CET for the EU audience.
