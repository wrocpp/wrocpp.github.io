# One function fills any struct

## Body
Every time you write a parser by hand you write the same shape twice: once as a pattern with capture groups, and once as the struct those captures fill. Then the assignment restates it a third time, in order, by hand.

C++26 reflection can read the struct's fields, so the third copy is unnecessary:

  template <typename T, ctll::fixed_string Pattern>
  constexpr std::optional<T> parse_into(std::string_view s) {
      auto m = ctre::match<Pattern>(s);
      if (!m) { return std::nullopt; }
      constexpr auto members = ... nonstatic_data_members_of(^^T, ctx);
      T out{};
      // capture I+1 goes to member I; capture 0 is the whole match
      ...
      return out;
  }

Two unrelated structs, one helper, no code per type. A date and a host-port pair both fill from their own patterns, and a non-matching input returns nullopt rather than a half-filled struct.

Why positional rather than by name? That was the version I tried first and it does not compose. CTRE addresses a named capture as get<"year">(), where the name is a template argument. Reflection hands you an identifier as a value, from identifier_of. Getting from one to the other means turning a reflected value back into a template parameter, and the straightforward spellings do not survive the trip.

Positional assignment sidesteps it, and the constraint is mild: the captures have to appear in the same order as the members. For a pattern and a struct written together, they already do.

The helper is about fifteen lines and replaces a category of code rather than a specific function. Most configuration handling, most log processing, and a good deal of protocol work has this shape.

Episode 7 of the CTRE series: https://wrocpp.github.io/posts/ctre-reflection/

## Hashtags
#cpp #cplusplus #cpp26 #reflection #metaprogramming

## Alt-text
A wro.cpp card reading "One function fills any struct", about combining CTRE with C++26 reflection.

## Suggested post time
Saturday 2026-10-03, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
