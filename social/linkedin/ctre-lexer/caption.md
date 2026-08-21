# A lexer that is one pattern

## Body
Hand-written lexers are mostly a loop, a switch, and careful index arithmetic. Regex-based ones usually cost an allocation per token and a pattern compilation at startup. CTRE gives a third option with neither.

The shape is one alternation with one capture per token kind, so the pattern doubles as the token table. Whichever capture engaged tells you what you matched.

Running it over "total = price * 3 + tax_rate" gives the expected stream, with whitespace dropped by the sink rather than the pattern.

It is built on tokenize rather than search_all, and that is deliberate. Feed the lexer "ok then #bad" and it produces [ok] [then] and stops, because # matches no branch. That is the correct failure. A lexer that skipped the # would hand the parser a token stream that looks valid and describes a program the author did not write.

It also runs at compile time, so counting tokens in a constant expression works and a static_assert can check the result. More useful than it first appears: a domain-specific string embedded in your source, a format specifier, a query template, can be lexed during compilation and rejected then, rather than parsed on every call at run time.

One detail cost me two compiles. The operator character class is written with the dash escaped. PCRE treats a dash at the start or end of a class as a literal; CTRE accepts neither position and rejects the pattern at compile time, naming the exact offset.

Episode 6 of the CTRE series: https://wrocpp.github.io/posts/ctre-lexer/

## Hashtags
#cpp #cplusplus #compilers #parsing #regex

## Alt-text
A wro.cpp card reading "A lexer that is one pattern", about building a tokeniser with CTRE.

## Suggested post time
Saturday 2026-09-26, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
