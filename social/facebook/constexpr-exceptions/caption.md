# C++26 lets you throw and catch at compile time

## Body
constexpr has spent four standards absorbing the rest of the language, but throwing stayed outside. Reach a throw during constant evaluation and the expression was not constant, so the build failed on the spot. That split error handling in two: a function meant for both compile time and runtime could not use the language's own error mechanism.

C++26 removes the split. A throw that is caught within the same constant evaluation is fine; only one that escapes fails the build.

The demo is a checked division that throws on a zero divisor and a wrapper that catches it. Both static_asserts pass, including the one where the exception is thrown and caught entirely at compile time. Nothing about it survives into the binary.

The win: one parser, one validation routine, one units conversion that behaves correctly whether it runs early or late.

Running on GCC 16.1: https://wrocpp.github.io/posts/constexpr-exceptions/

## Hashtags
#cpp #cplusplus #cpp26 #constexpr #programming

## Alt-text
A cream wro.cpp social card reading "Throw and catch before the program runs", about C++26 constexpr exceptions.

## Suggested post time
Tuesday 2026-09-01, 10:00 CET
Reason: Tuesday mid-morning CET for the EU audience.
