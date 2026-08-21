# A bad version string that fails the build

## Body
A regex that runs at compile time sounds like a parlour trick until you notice what it replaces: the class of bug where a hardcoded string is subtly wrong and nobody finds out until that code path runs.

CTRE matches are usable in constant expressions, so this is a build error rather than a runtime surprise:

  static_assert(is_semver("1.2"));   // fails: two components, not three

The demo is written so it cannot cheat. Every check is a static_assert and the validator is consteval rather than constexpr, which means it cannot be called at run time at all. If the matcher were not running during translation the file would not compile.

Parsing works the same way. The captures are ordinary string_views into the literal, so they work in a constant expression like anything else, and a version string becomes three integers the compiler already knew.

One detail that caught me while writing it: a constexpr function may be called at run time, so it cannot forward its parameter to a consteval one. The compiler is right and the fix is to say what you meant. If the check only ever happens during compilation, the function is consteval.

Version strings are the small example. The shape generalises to anything spelled as a literal and structured by convention: a route table, a set of environment variable names, an identifier format your team agreed on. Each of those is usually checked by a comment, a code review, or a test that runs long after the mistake was typed.

Episode 3 of the CTRE series: https://wrocpp.github.io/posts/ctre-compile-time/

## Hashtags
#cpp #cplusplus #constexpr #regex #compiletime

## Alt-text
A wro.cpp card reading "A bad version string that fails the build", about compile-time regex validation.

## Suggested post time
Saturday 2026-09-05, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
