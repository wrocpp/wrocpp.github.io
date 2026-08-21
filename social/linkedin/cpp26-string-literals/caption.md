# One compiler enforces half a rule

## Body
Some string literals never become objects. The text in static_assert, [[deprecated]], extern "C" and asm is read by the compiler and never encoded into anything. C++26 calls these unevaluated strings and makes two things ill-formed in them: an encoding prefix, and a numeric escape.

Neither ever meant anything. There is no encoding to apply and no byte to escape into. Tightening this costs nobody anything.

Except that the compilers disagree about how much of it is in force. This line is ill-formed under the paper:

  static_assert(sizeof(int) >= 2, "needs \x07 at least two bytes");

GCC 16.1 compiles it and runs the program. clang 22.1 rejects it:

  error: invalid escape sequence '\x07' in an unevaluated string literal

Both reject the encoding prefix. Only clang follows through on escapes. So GCC has half the rule.

The diagnostics differ too. clang names the concept the paper introduced. GCC says "a wide string is invalid in this context", which is true and leaves you to work out which context and why.

Does it matter directly? Barely. Writing u8 on a static_assert message is not a thing people do on purpose, and a \x07 in an assertion message is a typo.

Indirectly it is a reminder worth having: a paper being in the standard, and having a feature-test macro, says nothing about how much of it your compiler implements. This is a two-clause rule that landed years ago, and today one major compiler enforces one clause.

Both compilers, same file: https://wrocpp.github.io/posts/cpp26-string-literals/

## Hashtags
#cpp #cplusplus #cpp26 #gcc #clang #conformance

## Alt-text
A wro.cpp card reading "One compiler enforces half a rule", about C++26 unevaluated string literals.

## Suggested post time
Sunday 2026-10-18, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
