# Derive eq + hash + ordering from struct shape

## Body
C++20's `bool operator==(T const&) const = default` covers two-thirds of what value types need. The missing third is `std::hash<T>` -- which still requires a manual specialisation for every aggregate you put in an `unordered_map` -- and per-field customisation (skip a field, compare a `double` within epsilon, normalise a string before hashing) that defaulted ops can't express.

C++26 reflection fills both gaps. One header (`reflect_eq`):

```cpp
template <typename T>
struct std::hash<T> {  // for any reflectable aggregate
    constexpr std::size_t operator()(T const& x) const noexcept {
        std::size_t h = 0;
        template for (constexpr auto m : nonstatic_data_members_of<T>()) {
            h ^= std::hash<[:type_of(m):]>{}(x.[:m:]) + 0x9e3779b9 + (h<<6) + (h>>2);
        }
        return h;
    }
};
```

Rename a field -- hash follows. Add a member -- it's included. Same shape with annotations for opt-in customisation: `[[skip_in_hash]]`, `[[approx_eq(0.001)]]`, `[[normalise_first]]` mark per-field policy that the generic `operator==` and `hash` honor at compile time. Schema-as-spec: edit the struct, the comparison and hash stay correct.

The post also covers the gotchas: float comparison defaults are fragile (use epsilon annotations); std::hash mixing with the FNV-style boilerplate above is OK for hashmaps but NOT for cryptographic use; defaulted `operator<=>` interacts subtly with annotated equality.

What this replaces: every hand-maintained `std::hash<T>` specialisation, every "did I update both eq and hash when I added a field?" review comment.

Series post 7 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with GCC 16.1.

https://wrocpp.github.io/posts/derive-eq-hash/

## Hashtags
#cpp #cpp26 #reflection #hash #equality #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Derive eq + hash + ordering from struct shape". Subhead: Reflection fills the std::hash gap that C++20's defaulted operator== left; per-field annotations for epsilon, normalisation, skip. Citation: wro.cpp 2026-05-09.

## Suggested post time
Saturday 2026-05-09, 10:00 CET
Reason: Saturday morning catches weekend reading-list builders. Reflection-arc post 7; consistent every-other-day cadence.
