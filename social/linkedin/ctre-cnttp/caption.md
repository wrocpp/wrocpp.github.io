# One C++20 feature, one readable API

## Body
Why can you write this?

  ctre::match<"[a-z]+([0-9]+)">(subject)

A string literal, sitting where a type or a number usually goes. That spelling was impossible before C++20.

Non-type template parameters have always been restricted: integers, enumerators, pointers with linkage, not much else. A string literal was firmly outside, because the rules had no way to compare two of them for template-argument equivalence.

P0732 widened it to class types whose members are all public and themselves usable this way, with P1907 repairing the specification afterwards. That is enough for a small struct holding a character array, which is exactly what ctll::fixed_string is. Once such a type can be a template parameter, the pattern can travel as a template argument.

Before C++20 you wrote:

  static constexpr auto pattern = ctll::fixed_string{"[a-z]+([0-9]+)"};
  if (auto m = ctre::match<pattern>(subject)) { ... }

The older form is not dead history, by the way. I checked: it still compiles under -std=c++17 on current CTRE with both GCC and clang. What C++17 cannot do is the direct-literal spelling.

The feature did not make anything newly possible. It removed a naming ceremony that discouraged using the library in small ways, which turns out to matter more than it sounds when you are writing three patterns in one function.

One trap worth knowing, because the error is unhelpful: naming a pattern means naming a ctll::fixed_string. A plain constexpr auto holding a string literal is a const char pointer, and a pointer to a string literal is not a valid template argument.

Episode 2 of the CTRE series, both spellings compiling side by side: https://wrocpp.github.io/posts/ctre-cnttp/

## Hashtags
#cpp #cplusplus #cpp20 #templates #regex

## Alt-text
A wro.cpp card reading "One C++20 feature, one readable API", about class types as non-type template parameters.

## Suggested post time
Saturday 2026-08-29, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
