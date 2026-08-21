# Compile-time regex has a compile-time bill

## Body
Seven episodes of what CTRE does well earns one about what it costs.

Build time first, measured rather than asserted. Compiling N distinct patterns on GCC 16.1:

  0 patterns (header only)   724 ms
  1                         1374 ms
  5                         1771 ms
  10                        2237 ms
  20                        4206 ms

Two things stand out. Including the header at all costs about three quarters of a second before you write a single pattern. After that the growth is roughly linear, very approximately a hundred milliseconds per pattern.

The honest caveat: these were measured on Compiler Explorer, a shared machine, and repeated runs moved by nearly a factor of two. A 40-pattern measurement came out barely above the 20-pattern one, which is not plausible as real scaling and is better read as noise. Treat the shape as the finding and measure your own hardware before deciding anything.

None of that is alarming for a program with a handful of patterns. It matters if you are tempted to put CTRE in a widely included header, which turns the fixed cost into a per-translation-unit cost across the build.

Then syntax. The library is almost PCRE compatible, and the gaps you find by compiling rather than reading. A bare dash inside a character class is rejected at either end, where PCRE takes it as a literal.

And the error message. Get a pattern wrong and it fails at compile time, which is the point, but the delivery is a diagnostic about an incomplete type with the offset encoded in the type name. The information is precise; the presentation is what C++26's user-generated static_assert messages exist to fix.

Final episode: https://wrocpp.github.io/posts/ctre-costs/

## Hashtags
#cpp #cplusplus #performance #compiletime #regex

## Alt-text
A wro.cpp card reading "Compile-time regex has a compile-time bill", about CTRE build costs and limits.

## Suggested post time
Saturday 2026-10-10, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
