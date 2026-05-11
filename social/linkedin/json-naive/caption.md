# A 40-line JSON serializer in C++26

## Body
JSON serialization in C++ used to be either heavy (`nlohmann/json` -- one of the world's most popular C++ libraries, but a transitive dependency in everything), or hand-rolled (write `operator<<` per type, repeat forever). Both stop you from understanding what a serializer is.

C++26 reflection turns it into a teaching exercise. Forty lines walk any aggregate at compile time and emit a complete JSON writer. Add a field, the JSON follows. Nest a struct, the JSON nests. Drop a vector, the JSON arrays.

```cpp
template <typename T>
constexpr std::string to_json(T const& v) {
    if constexpr (std::is_aggregate_v<T>) {
        std::string out = "{";
        bool first = true;
        constexpr auto ctx = std::meta::access_context::unchecked();
        template for (constexpr auto m
                      : std::define_static_array(
                          std::meta::nonstatic_data_members_of(^^T, ctx))) {
            if (!first) out += ',';
            first = false;
            out += std::format("\"{}\":", std::meta::identifier_of(m));
            out += to_json(v.[:m:]);
        }
        return out + '}';
    } else if constexpr (std::is_arithmetic_v<T>) return std::format("{}", v);
    else if constexpr (std::same_as<T, std::string>) return std::format("\"{}\"", v);
    // ... arrays, optionals, ranges
}
```

What this replaces in everyday C++: the per-type serializer overhead, the codegen step (no `nlohmann::adl_serializer` specialisations), the dependency on the JSON library's evolution. What it does NOT replace: production-grade libraries like Glaze v7.2 (already on P2996, faster than serde_json on real payloads), nlohmann/json (gigantic ecosystem, edge cases polished over a decade), or anything that needs SAX/streaming, error recovery, schema validation. The 40-line version is for understanding -- and for the surprising number of internal-only schemas where it's enough.

Series post 8 of 25 in the wro.cpp C++26 reflection arc. Cross-link: post 5 (enum-to-string), post 9 (annotations -- adds `[[=json::skip{}]]` + `[[=json::rename{"id"}]]` to this same walker), post 10 (the inverse: JSON -> struct with `std::expected` errors).

https://wrocpp.github.io/posts/json-naive/

## Hashtags
#cpp #cpp26 #reflection #json #serialization #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "A 40-line JSON serializer in C++26". Subhead: One template walks any aggregate; arrays nest, vectors arrayify, optionals null-or-emit. Citation: wro.cpp 2026-05-11.

## Suggested post time
Monday 2026-05-11, 18:00 CET (recovery slot)
Reason: Original morning fire slot missed; afternoon EU recovery slot still catches engagement before the next-day reading list builds.
