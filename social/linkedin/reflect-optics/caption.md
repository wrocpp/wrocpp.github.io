# reflect_optics: Haskell-style lenses for C++26

## Body
Haskell's `lens` library has been the gold standard for nested data access for fifteen years. It lets you `view`, `set`, and `over` nested fields without writing the access path five times. Ports to C++ needed macro hell and never felt right -- until reflection.

```cpp
struct Address { std::string city; int postal_code; };
struct Person  { std::string name; Address home; int age; };

Person p{"Filip", {"Wroclaw", 50001}, 40};

auto city_lens = field<"home"> | field<"city">;

std::println("view: {}", view(city_lens, p));         // Wroclaw
auto p2 = set(city_lens, p, "Warsaw");
std::println("set:  {}", view(city_lens, p2));        // Warsaw
auto p3 = over(field<"home"> | field<"postal_code">, p, [](int x){ return x+1; });
std::println("over: {}", view(field<"home"> | field<"postal_code">, p3)); // 50002
```

The mechanic: each `field<"name">` resolves at compile time via reflection -- splice the matching member to a pointer-to-data-member, build a lens whose getter / setter operate through `obj.*pmd`. Composition with `operator|` chains pointer-to-data-member dereferences. Zero overhead at runtime; the optimiser sees the chain as straight-line `obj.home.city` access.

What this UNLOCKS: deep partial updates without `obj.home.city = ...; obj.home.country = ...; obj.timestamp = clock();` repetition. State management for redux-style stores. Diff-and-patch on configuration trees. Functional optics pipelines without paying for the abstraction.

What this does NOT replace: domain-specific accessors with validation logic (a setter that checks invariants), C++-Core-Guidelines-style getters/setters that hide implementation details, lazy access patterns. Lenses are for the case where the field IS the interface.

The same `nonstatic_data_members_of` walker drives the [auto formatter](/posts/auto-formatter/), the [JSON serialiser](/posts/json-naive/), the [reflect_llmschema](/posts/reflect-llmschema/), and the [reflect_arbitrary](/posts/reflect-arbitrary/). One walker, five output shapes -- print, serialise, schema, generate, optic.

Series post 21 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996.

https://wrocpp.github.io/posts/reflect-optics/

## Hashtags
#cpp #cpp26 #reflection #lens #optics #functional #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_optics". Subhead: Haskell-style composable lenses for C++26 -- view / set / over nested fields with operator|. Citation: wro.cpp 2026-06-21.

## Suggested post time
Sunday 2026-06-21, 10:00 CET
Reason: Sunday morning EU C++ + functional-curious audience; reflection-arc post 21 continues the every-2-day cadence.
