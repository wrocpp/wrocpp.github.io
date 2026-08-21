# One C++20 feature, one readable API

## Body
Why can you write ctre::match<"[a-z]+([0-9]+)">(subject)? Because C++20 allowed class types as non-type template parameters.

Before that, a string literal could not be a template argument, so the pattern needed a name and a constexpr variable of a small literal class type. P0732 changed it, P1907 repaired the wording, and the pattern can now travel as a template argument directly.

The older spelling still works, and I checked: it still compiles under C++17 on current CTRE. What C++17 cannot do is put the literal straight in the angle brackets.

Episode 2 of the CTRE series, both spellings side by side: https://wrocpp.github.io/posts/ctre-cnttp/

## Hashtags
#cpp #cplusplus #cpp20 #programming

## Alt-text
A wro.cpp card about class types as non-type template parameters in C++20.

## Suggested post time
Saturday 2026-08-29, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
