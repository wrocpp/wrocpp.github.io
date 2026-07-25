# C++26 lets you throw and catch at compile time

## Body
constexpr has spent four standards absorbing the rest of the language. C++20 brought virtual calls, dynamic allocation, try blocks, and much of the algorithm library. What stayed outside was actually throwing: reach a throw during constant evaluation and the expression was simply not constant, so the build failed on the spot.

That split error handling in two. A function meant for both compile time and runtime could not use the language's own error mechanism. It needed a sentinel value, an optional, or a separate constexpr-only path.

C++26 removes the split. Exceptions can be thrown and caught during constant evaluation. A throw caught within the same evaluation is fine; only one that escapes to the top makes the expression non-constant.

The demo is a checked division that throws domain_error on a zero divisor, wrapped by a function that catches it and returns a sentinel. Both static_asserts pass, including:

  static_assert(try_div(10, 0) == -1);

At compile time the throw happens, the catch handles it, evaluation continues, and the result is an ordinary constant. No runtime, no exception tables, nothing left in the binary.

The practical win is one function serving both worlds: a parser, a units conversion, a validation routine can throw and behave correctly in a static_assert or at runtime, with no duplicated logic. It also improves failure messages, since the compiler can name the exception and the throw site instead of producing a wall of template instantiation noise.

Running on GCC 16.1: https://wrocpp.github.io/posts/constexpr-exceptions/

Where would compile-time error handling clean up your code?

## Hashtags
#cpp #cplusplus #cpp26 #constexpr #metaprogramming #programming

## Alt-text
A cream wro.cpp social card reading "Throw and catch before the program runs", about C++26 constexpr exceptions.

## Suggested post time
Tuesday 2026-09-01, 10:00 CET
Reason: Tuesday mid-morning CET, a strong weekday slot.
