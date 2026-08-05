# Two compilers, one float-to-int cast, two different wrong answers

## Body
static_cast<int>(some_double) is one of the most ordinary lines in C++. It is also undefined behavior whenever the truncated value will not fit, and whenever the source is NaN. The standard does not say the result is unspecified or implementation-defined. It imposes no requirement at all.

The usual defences do not help. No compiler warns by default, and gsl::narrow guards integer-to-integer narrowing but not this case.

So I ran the same program on both compilers.

GCC prints 1e18 as -2147483648. Clang prints 0. One source file, one standard, two toolchains, two different answers, and neither is wrong because there is no right answer to be wrong about. If you ever wrote a clamp that relied on out-of-range values saturating to INT_MIN, it works on one compiler and quietly does something else on the other.

Then the detail that actually matters in practice. Clang includes float-cast-overflow in -fsanitize=undefined. GCC does not. GCC deliberately leaves it out of the umbrella option, so a project that dutifully enables -fsanitize=undefined in CI and builds with GCC is not checking these casts at all. You have to name the check.

The fix is a range test done in floating point, before the conversion, with isfinite to reject NaN and the infinities.

Both demos run live: https://wrocpp.github.io/posts/float-to-int-ub/

Is float-cast-overflow enabled in your CI?

## Hashtags
#cpp #cplusplus #undefinedbehavior #sanitizers #debugging #programming

## Alt-text
A cream wro.cpp social card reading "Same cast, two compilers, two answers", about float-to-int undefined behavior.

## Suggested post time
Saturday 2026-08-08, 10:00 CET
Reason: weekend mid-morning suits a longer correctness read.
