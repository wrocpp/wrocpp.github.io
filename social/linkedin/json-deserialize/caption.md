# JSON -> struct with std::expected errors

## Body
Post 8 was the easy direction: walk a struct, emit JSON. Post 10 is the hard one: take untrusted JSON bytes, build a struct, fail closed on type mismatch / missing field / unknown key.

Reflection drives the walker the same way, but the failure path is where the production-grade work happens:

```cpp
struct User { std::string name; int age; bool admin; };

auto r = rjson::parse<User>(R"({"name":"Filip","age":40,"admin":true})");
// std::expected<User, parse_error>
r.value().name;  // "Filip"

auto bad = rjson::parse<User>(R"({"name":"Filip","age":"forty","admin":true})");
// bad.error() == parse_error{ path: ".age", expected: "number", got: "string" }
```

Three things this gets right that hand-rolled deserializers usually don't:

1. **`std::expected<T, parse_error>`** -- no exceptions, no out-parameters, no exit code conventions. Caller pattern-matches on success/failure.
2. **Path-aware error reporting** -- `.users[3].address.postal_code` not "parse error". Reflection knows the field name; the recursive walker accumulates the path automatically.
3. **Fail-closed on unknown fields** -- protects against trust-boundary attacks (extra fields in attacker-controlled payloads) by default; opt-in `[[=json::allow_unknown{}]]` annotation when you genuinely want lenient parsing.

What this does NOT replace: nlohmann/json (mature error recovery, JSON Pointer support, deep ecosystem), Glaze (faster + already on P2996), simdjson (raw speed). The reflection-driven deserializer is for the common case where you control both ends and want type-safe parsing with clean errors. The same walker grows annotations for renaming, default values, and skip behaviour -- post 9 covers those.

Series post 10 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/json-deserialize/

## Hashtags
#cpp #cpp26 #reflection #json #expected #deserialize #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "JSON to struct with std::expected errors". Subhead: Reflection-driven deserialiser with path-aware error reporting and fail-closed unknown-field rejection. Citation: wro.cpp 2026-05-15.

## Suggested post time
Friday 2026-05-15, 10:00 CET
Reason: Friday morning slot; reflection-arc post 10 continues the 2-day cadence.
