# Goodbye magic_enum: enum reflection done right

## Body
`magic_enum` is one of the cleverest tricks in modern C++. It gives you `enum` <-> string by parsing `__PRETTY_FUNCTION__` in a constexpr loop over a fixed integer range. Brilliant. Limited.

Three things break the trick: range-bound (default `[-128, 128]`; widening costs compile-time), compiler-specific (parses `__PRETTY_FUNCTION__` and breaks on format changes), and powerless against flags enums whose combined values aren't in the declared range.

C++26 reflection (P2996) collapses all of it. `enumerators_of(^^E)` returns the actual enumerator list straight from the compiler. No range, no format parsing, no knob.

The whole library, including flags round-trip, is 30 lines:

```cpp
template <typename E>
constexpr std::string_view to_string(E value) {
    template for (constexpr auto e : enumerators_of_static<E>()) {
        if ([:e:] == value) return std::meta::identifier_of(e);
    }
    return "<unknown>";
}

template <typename E>
constexpr std::optional<E> from_string(std::string_view name) {
    template for (constexpr auto e : enumerators_of_static<E>()) {
        if (std::meta::identifier_of(e) == name) return E{[:e:]};
    }
    return std::nullopt;
}
```

The flags inverse `from_flags_string<Permission>("read|write")` falls out as a ranges chain: `std::views::split('|')` for tokenisation, `std::ranges::fold_left` (C++23) over `std::optional<U>`, monadic `.and_then` / `.transform` propagating the fail-closed step. Typo at the boundary returns `std::nullopt` rather than a silently-zero mask. The post shows the imperative-equivalent loop side-by-side so the ranges form is readable for first-time readers.

What you gain: unbounded range, no compile-time knob, single compiler-agnostic path. Production-ready for enums whose enumerators are pure single-bit; the post documents the "combined enumerator" caveat to tighten before deploying when names like `Permission::all = 7` exist.

Series post 5 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with GCC 16.1 (`-std=c++26 -freflection`).

https://wrocpp.github.io/posts/enum-to-string/

## Hashtags
#cpp #cpp26 #reflection #magic_enum #enum #wrocpp #moderncpp #ranges

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Goodbye magic_enum: enum reflection done right". Subhead: A reflection-driven enum<->string library in 30 lines, with flags round-trip via std::ranges::fold_left + monadic optional. Citation: wro.cpp 2026-05-05.

## Suggested post time
Tuesday 2026-05-05, 10:00 CET
Reason: Mid-week morning slot for EU C++ engineers; series post launch traditionally fires at this slot to match the reflection-arc cadence.
