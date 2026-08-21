# The manual still teaches a deprecated call

## Body
CTRE has three ways to walk an input, and the documentation teaches a fourth that the compiler now warns about: ctre::range is deprecated in favour of search_all.

The distinction that matters is between search_all and tokenize. Same pattern, same input "ab!!cd":

  search_all  ->  [ab] [cd]
  tokenize    ->  [ab]

search_all skips what it cannot match. tokenize stops there. For scanning a log line, skipping is right. For lexing a language, unmatched input is a syntax error and silently skipping it turns a broken program into a subtly different valid one.

Episode 5: https://wrocpp.github.io/posts/ctre-ranges/

## Hashtags
#cpp #cplusplus #regex #programming

## Alt-text
A wro.cpp card about CTRE search_all, split and tokenize.

## Suggested post time
Saturday 2026-09-19, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
