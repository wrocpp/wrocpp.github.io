# The manual still teaches a deprecated call

## Body
Matching one string is the simple case. Most real uses walk an input, and CTRE has three ways to do that which are easy to confuse.

First, a documentation problem worth stating plainly. The readthedocs page teaches ctre::range and calls range support preliminary. Compile that today and the compiler disagrees:

  warning: 'ctre::range<...>' is deprecated: use search_all

The same page carries a literal "TODO more detailed regex information" where the syntax reference should be. Neither is a criticism of a library under active development, but it sets the working rule: read the header, not the manual.

search_all gives every match, skipping whatever lies between. split gives the pieces between matches of a separator. tokenize consumes the input from the front and stops at the first position where the pattern does not match.

That last distinction is the one that matters, and it is easy to miss. Same pattern, same input:

  search_all<"[a-z]+"> over "ab!!cd"  ->  [ab] [cd]
  tokenize<"[a-z]+">   over "ab!!cd"  ->  [ab]

search_all treats unmatched input as something to skip past. tokenize treats it as the end of the road.

For scanning a log line for every timestamp, skipping is correct. For lexing a language, unmatched input is a syntax error, and silently skipping it turns a broken program into a subtly different valid one. Stopping is the feature.

Episode 5 of the CTRE series: https://wrocpp.github.io/posts/ctre-ranges/

## Hashtags
#cpp #cplusplus #regex #ranges #documentation

## Alt-text
A wro.cpp card reading "The manual still teaches a deprecated call", about CTRE search_all, split and tokenize.

## Suggested post time
Saturday 2026-09-19, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
