# Handling overflow and division by zero without undefined behavior

## Body
INT_MAX + 1 and x / 0 are undefined for int. The tools that remove the undefined behavior apply three different policies, and this post runs each of them on GCC 16.2.

std::saturating_add clamps the result to INT_MAX, so the value changes. ckd_add from <stdckdint.h> returns the wrapped value and a flag, and the caller decides what to do. -ftrapv, or UBSan with -fsanitize-trap, stops the program. None of them is an operator on a single expression.

The post also has the exact runtime diagnostics, what -O0 and -O2 produced for the plain operations (including a build where -ftrapv did not trap), the constant-evaluation error texts, and which libraries ship the functions: libstdc++ yes, libc++ has the saturating functions but not the ckd feature macro, and the MSVC STL tracking issue was open. It was tested on GCC 16.2 and Compiler Explorer, not on MSVC.

https://wrocpp.github.io/posts/handle-overflow-and-division-by-zero-without-ub/

This is episode 3 of a series that started from a reader question about checking undefined behavior per statement.

## Hashtags
#cpp #cpp26 #undefinedbehavior #sanitizers #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "INT_MAX + 1 can clamp, report or trap" with a subtitle naming std::saturating_add, ckd_add and -ftrapv as three different policies run on GCC 16.2. Citation footer: wro.cpp, 2026-11-06.

## Suggested post time
Friday 2026-11-06, 08:00 UTC (09:00 CET)
Reason: one short post for the day, in the ub-checks-per-statement series.
