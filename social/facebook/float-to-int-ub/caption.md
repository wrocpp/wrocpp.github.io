# Two compilers, one float-to-int cast, two different wrong answers

## Body
static_cast<int>(some_double) is undefined behavior whenever the value will not fit, and for NaN. No compiler warns by default.

I ran the same program on both. GCC prints -2147483648. Clang prints 0. One source file, one standard, two different answers, and neither is wrong because there is no right answer to be wrong about.

The practical detail: Clang includes float-cast-overflow in -fsanitize=undefined, GCC does not. A project that enables -fsanitize=undefined in CI and builds with GCC is not checking these casts at all. You have to name the check.

Both demos run live: https://wrocpp.github.io/posts/float-to-int-ub/

## Hashtags
#cpp #cplusplus #undefinedbehavior #debugging #programming

## Alt-text
A cream wro.cpp social card reading "Same cast, two compilers, two answers", about float-to-int undefined behavior.

## Suggested post time
Saturday 2026-08-08, 10:00 CET
Reason: weekend mid-morning for a correctness read.
