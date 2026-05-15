# reflect_arbitrary: property-based test generators from struct shape

## Body
QuickCheck in Haskell, mockall in Rust, jqwik in Java -- every major language auto-derives `Arbitrary<T>` from a struct declaration. C++ was last. Reflection fixes that:

```cpp
struct User {
    std::string name;
    int         age;
    bool        admin;
    Address     home;       // recurses into nested structs
};

auto& gen = reflect_arbitrary::generator<User>();
for (int i = 0; i < 5; ++i) {
    User u = gen();
    std::println("{}", u);
}
// Generated User #0: name=okhu age=82 admin=false home={city=kxu pc=99}
// Generated User #1: name=vub  age=87 admin=true  home={city=ua  pc=75}
// ...
```

The mechanic: walk `nonstatic_data_members_of(^^T)` at compile time, recurse into each member's type, dispatch to a per-type primitive generator. Strings get random ASCII of bounded length; ints get a uniform distribution; bools get 50/50; nested aggregates recurse. Add a field, the generator updates. Add a custom type with a registered specialisation, it slots in.

The library ships adapters for both major C++ property-test frameworks: **RapidCheck** (the established choice) and **Google FuzzTest** (the structured-fuzzing successor). Same `T` definition, two test runners; the schema is the only declaration.

What this REPLACES: every hand-written `Arbitrary<MyStruct>` specialisation, every fuzzer-corpus seed your team has been hand-curating because "the harness needed a valid User", every test that papers over forgotten field updates with hardcoded fixtures.

What this does NOT replace: shrinking strategy (RapidCheck's strength), domain-specific generators (a `User::email` field probably needs a real email shape, not random ASCII), the property assertion itself (you still write the `forAll<User>([](User u) { ... })`). The reflection layer is the boilerplate-elimination half; the property is yours to write.

The same `nonstatic_data_members_of` walker drives the [auto formatter](/posts/auto-formatter/), the [JSON serialiser](/posts/json-naive/), the [reflect_llmschema](/posts/reflect-llmschema/) post that fired on Wednesday. One walker, four output formats. Property-based testing is the natural pair to the schema-generation pattern: same struct definition, mirror-image directions.

Series post 20 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996 (`-std=c++26 -freflection-latest -stdlib=libc++`).

https://wrocpp.github.io/posts/reflect-arbitrary/

## Hashtags
#cpp #cpp26 #reflection #propertytesting #quickcheck #rapidcheck #fuzztest #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_arbitrary". Subhead: QuickCheck-style generator from struct shape; RapidCheck + Google FuzzTest adapters. Citation: wro.cpp 2026-06-19.

## Suggested post time
Friday 2026-06-19, 10:00 CET
Reason: Friday morning EU C++ + testing audience; reflection-arc post 20 continues the every-2-day cadence.
