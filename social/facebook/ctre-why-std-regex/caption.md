# std::regex, measured fairly, still loses

## Body
Everyone knows std::regex is slow. Fewer people say by how much, or measured how.

I measured it against CTRE as charitably as I could: the std::regex object built once outside the timed loop, both sides extracting captures, both loop bodies guarded so the compiler cannot delete the work.

CPU time per match: std::regex 455 ns on GCC, CTRE 6.6 ns. About seventy times, on both compilers, in the setup that favours std::regex most.

First of an eight part series on compile time regular expressions.

Benchmark you can rerun: https://wrocpp.github.io/posts/ctre-why-std-regex/

## Hashtags
#cpp #cplusplus #performance #programming

## Alt-text
A wro.cpp card about benchmarking CTRE against std::regex.

## Suggested post time
Saturday 2026-08-22, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
