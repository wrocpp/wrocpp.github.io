# Destructuring a regex match

## Body
Three ways to get values out of a CTRE match: by number, by name, or by destructuring the result directly.

Named captures are checked against the pattern, so a typo is a compile error rather than an empty capture. Structured bindings read best when the pattern is genuinely a record, though they need a trailing test because the bindings are the captures.

C++26 removes that trailing test with P0963. At run time both compilers agree; in a constant expression only clang does, which I wrote up separately.

An unmatched capture converts to false, which is how you tell matched-empty from did-not-match, and is the basis of building a lexer from one pattern.

Episode 4: https://wrocpp.github.io/posts/ctre-captures-bindings/

## Hashtags
#cpp #cplusplus #regex #programming

## Alt-text
A wro.cpp card about CTRE captures and structured bindings.

## Suggested post time
Saturday 2026-09-12, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
