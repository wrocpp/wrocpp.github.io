# A lexer that is one pattern

## Body
A lexer built from one pattern, with no allocation and no runtime regex compilation.

One alternation, one capture per token kind, so the pattern doubles as the token table. Whichever capture engaged tells you what you matched.

It uses tokenize rather than search_all deliberately. Feed it "ok then #bad" and it produces [ok] [then] and stops, because # matches no branch. That is the correct failure: a lexer that skipped it would hand the parser a stream that looks valid and describes a different program.

It runs at compile time too, so a static_assert can check the token count.

Episode 6: https://wrocpp.github.io/posts/ctre-lexer/

## Hashtags
#cpp #cplusplus #parsing #programming

## Alt-text
A wro.cpp card about building a tokeniser with CTRE.

## Suggested post time
Saturday 2026-09-26, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
