# One compiler enforces half a rule

## Body
C++26 makes encoding prefixes and numeric escapes ill-formed in unevaluated strings, the ones in static_assert, [[deprecated]] and asm that never become objects.

The compilers disagree about how much of that is in force. This is ill-formed per the paper:

  static_assert(sizeof(int) >= 2, "needs \x07 at least two bytes");

GCC 16.1 compiles and runs it. clang 22.1 rejects it. Both reject the encoding prefix; only clang follows through on escapes.

The point is not the rule, which nobody trips over on purpose. It is that a paper being in the standard says nothing about how much of it your compiler implements.

Both compilers, same file: https://wrocpp.github.io/posts/cpp26-string-literals/

## Hashtags
#cpp #cplusplus #cpp26 #programming

## Alt-text
A wro.cpp card about C++26 unevaluated string literals.

## Suggested post time
Sunday 2026-10-18, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
