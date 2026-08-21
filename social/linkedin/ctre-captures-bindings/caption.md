# Destructuring a regex match

## Body
A match object answers two questions at once: did it match, and what did it capture. CTRE gives three ways to ask the second one.

By number, where index 0 is the whole match and groups follow the order their opening parenthesis appears. Fine for one or two groups; past that, get<4> in code someone reads six months later is a small puzzle every time.

By name, where the name lives in the pattern and is checked against it, so a typo is a compile error rather than an empty capture. This is the same C++20 feature from episode 2 doing a second job: the name reaches get as a template argument.

By destructuring, which reads best when the pattern is genuinely a record:

  if (auto [whole, y, m, d] = ctre::match<R"((\d{4})/(\d{1,2})/(\d{1,2}))">(s); whole) { ... }

Note the trailing test. The bindings are the captures, so checking success needs the whole-match binding explicitly.

C++26 removes that with P0963, letting the binding declaration itself be the condition. At run time it works on GCC 16.1 and clang 22.1 alike. Inside a constant expression it currently works on clang only, and I wrote up that divergence separately because the reduced case is twenty lines.

One more thing worth knowing: an unmatched capture converts to false, which is how you distinguish matched-empty from did-not-match. That is the whole basis of building a lexer from one pattern, which is two episodes away.

Episode 4 of the CTRE series: https://wrocpp.github.io/posts/ctre-captures-bindings/

## Hashtags
#cpp #cplusplus #cpp26 #regex #structuredbindings

## Alt-text
A wro.cpp card reading "Destructuring a regex match", about CTRE captures and structured bindings.

## Suggested post time
Saturday 2026-09-12, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
