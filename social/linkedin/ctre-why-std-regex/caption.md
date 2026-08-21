# std::regex, measured fairly, still loses

## Body
Everyone knows std::regex is slow. Rather less often does anyone say by how much, against what, and measured how.

So I measured it, as fairly as I could manage. The comparison is against CTRE, Hana Dusikova's compile time regular expression library, and three decisions matter more than the numbers:

The std::regex object is built once, outside the timed loop. Building it per iteration would measure pattern parsing every time, which is the least flattering thing you can do to it. Steady state matching is where std::regex looks best.

Both sides extract captures, so neither is quietly doing less work.

Both loop bodies are wrapped in DoNotOptimize. That matters more than usual here, because CTRE resolves the pattern at compile time and an unguarded loop can fold away entirely and report a spectacular result for doing nothing.

CPU time per operation:

  std::regex, pattern built once   455 ns on GCC, 319 ns on clang
  CTRE                             6.6 ns on GCC, 4.5 ns on clang

About seventy times, on both compilers, in the setup that favours std::regex most. Include construction, which one shot validation actually pays, and it reaches roughly a thousand times.

This opens an eight part series. CTRE is interesting beyond being fast: almost every part of its interface exists because a specific language feature landed, which is the thread the rest of the series follows.

Benchmark you can rerun in a browser: https://wrocpp.github.io/posts/ctre-why-std-regex/

## Hashtags
#cpp #cplusplus #performance #regex #benchmarking

## Alt-text
A wro.cpp card reading "std::regex, measured fairly, still loses", about benchmarking CTRE against std::regex.

## Suggested post time
Saturday 2026-08-22, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
