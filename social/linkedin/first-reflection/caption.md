# Your first ^^: reflecting types and walking members

## Body
The hardest part about C++26 reflection isn't the syntax. It's the muscle memory.

For 25 years we simulated reflection through templates, Boost.Hana, and code-generation glue. Now you write `^^Point` and get back a `std::meta::info`, an opaque compile-time handle. Hand it to `nonstatic_data_members_of` and the compiler gives you the fields.

Twelve lines turn into a "describe any struct" utility:

```
template <typename T>
consteval auto describe() {
    std::string out;
    constexpr auto ctx = std::meta::access_context::unchecked();
    for (auto m : std::meta::nonstatic_data_members_of(^^T, ctx)) {
        out += std::meta::identifier_of(m);
        out += ": ";
        out += std::meta::display_string_of(std::meta::type_of(m));
        out += '\n';
    }
    return out;
}
```

Run on `struct Point { int x; int y; };` and you get back `x: int / y: int`. No header beyond `<experimental/meta>`. No macros. No `#define BOOST_...`.

This is part 2 of the wro.cpp reflection series. It builds the primitives that the part-1 teaser leaned on. The next post adds splicing, turning a reflection back into code that actually reads `p.x` for a runtime `p`.

Read it: https://wrocpp.github.io/posts/first-reflection/

What's the smallest reflection-powered utility you'd write first? Drop it in the comments.

## Hashtags
#cpp #cpp26 #reflection #p2996 #moderncpp #compiletime #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline reads "Your first ^^." with the carets in orange and the period in blue. Subtitle: twelve lines walk any struct's members at compile time, no macros or Boost.Hana.

## Suggested post time
Wednesday 2026-05-13, 10:00 CET
Reason: matches the post's pubDate so the teaser lands the same day the link goes live, and Wednesday morning catches European C++ engineers mid-week scroll.
