# Reflect_print: auto std::formatter for any aggregate

## Body
Rust gives you `#[derive(Debug)]`. C++ gave you `operator<<` per type, written by hand. C++26 reflection closes the gap with one header.

`reflect_print<T>` walks any aggregate at compile time and emits a `std::format` specialisation that prints all fields with their names. Recursive: nested aggregates are formatted in turn. Add a field, the print follows automatically. No hand-maintained overload, no codegen step.

```cpp
struct Address { std::string city; int postal_code; };
struct User { std::string name; int age; bool admin; Address home; };

User u{"Filip", 40, true, {"Warsaw", 12345}};
std::println("{}", u);
// User{name: Filip, age: 40, admin: true, home: Address{city: Warsaw, postal_code: 12345}}
```

The trick is a `template <typename T> struct std::formatter` specialisation written ONCE for any aggregate, with the field walk inside `format()` driven by `nonstatic_data_members_of(^^T)`. Rename a field and the print follows. Add an int member and it shows up. Remove one and it disappears. The string output is structural, not editorial; for journals and audit logs that's exactly what you want.

What this replaces: every `operator<<(std::ostream&, T const&)` overload in your codebase, plus all the `fmt::format` per-type specialisations you've been maintaining.

What this does NOT replace: hand-tuned print formats (custom field separators, omitting boilerplate fields, redacting secrets). Those still need a manual `std::formatter` specialisation. The default exists for the common case: structured printing of every field, every time, kept in sync with the schema.

Series post 6 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with GCC 16.1 (`-std=c++26 -freflection`).

https://wrocpp.github.io/posts/auto-formatter/

## Hashtags
#cpp #cpp26 #reflection #format #fmt #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Reflect_print: auto std::formatter for any aggregate". Subhead: One header replaces every operator<< and fmt specialisation; nested aggregates print recursively. Citation: wro.cpp 2026-05-07.

## Suggested post time
Thursday 2026-05-07, 10:00 CET
Reason: Mid-week morning slot reaches EU C++ engineers in flow. Reflection-arc post 6 follows post 5's launch on Tue 5/5; consistent every-other-day cadence.
