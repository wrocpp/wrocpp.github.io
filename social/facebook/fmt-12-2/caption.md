# {fmt} can do the whole format at compile time

## Body
std::format checks your format string at compile time. What it still does at runtime is parse it.

{fmt} can do that during compilation too. Wrap the string in FMT_COMPILE and the parse happens once, emitting straight-line formatting code, so the whole call becomes a constant expression. Width, zero-fill and field order are all resolved before the program runs. On a hot path with a fixed layout, that removes the parse from every call.

The 12.2 release also adds a type-safe C formatting API, a proper C++20 module target, and the full Dragonbox cache by default for faster float formatting.

Runs live on Compiler Explorer: https://wrocpp.github.io/posts/fmt-12-2/

## Hashtags
#cpp #cplusplus #fmt #performance #programming

## Alt-text
A cream wro.cpp social card reading "A format call that costs nothing at runtime", about FMT_COMPILE and fmt 12.2.

## Suggested post time
Wednesday 2026-08-12, 10:00 CET
Reason: midweek mid-morning CET.
