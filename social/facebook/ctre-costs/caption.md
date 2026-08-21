# Compile-time regex has a compile-time bill

## Body
Seven episodes on what CTRE does well earns one on what it costs.

Compiling N distinct patterns on GCC 16.1: the header alone is about 724 ms before you write a single pattern, then roughly a hundred milliseconds per pattern after that. Measured on a shared machine, so treat the shape as the finding rather than the exact figures.

That is fine for a handful of patterns and matters if you put CTRE in a widely included header, where the fixed cost multiplies across translation units.

Also: a bare dash inside a character class is rejected at either end, where PCRE takes it as a literal. The kind of gap you find by compiling rather than reading.

Final episode: https://wrocpp.github.io/posts/ctre-costs/

## Hashtags
#cpp #cplusplus #performance #programming

## Alt-text
A wro.cpp card about CTRE build costs and limits.

## Suggested post time
Saturday 2026-10-10, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
