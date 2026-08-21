# A bad version string that fails the build

## Body
CTRE matches run in constant expressions, so a regex can validate a string literal while the compiler is still working:

  static_assert(is_semver("1.2"));   // fails the build

The demo cannot cheat: every check is a static_assert and the validator is consteval, so it cannot be called at run time at all.

The captures are ordinary string_views into the literal, so parsing works too, and a version string becomes three integers the compiler already knew.

The shape generalises to anything spelled as a literal and structured by convention, which is usually checked by a comment or a test that runs long after the mistake was typed.

Episode 3 of the CTRE series: https://wrocpp.github.io/posts/ctre-compile-time/

## Hashtags
#cpp #cplusplus #constexpr #programming

## Alt-text
A wro.cpp card about compile-time regex validation.

## Suggested post time
Saturday 2026-09-05, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
