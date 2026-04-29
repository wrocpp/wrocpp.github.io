# template for: iterating reflections at compile time

## Body
C++26 reflection has three primitives. Posts 2 + 3 covered two of them (`^^T` and `[: r :]`). The third is the loop.

`template for` is an *expansion statement* (proposal P1306): the compiler unrolls the loop at compile time and instantiates the body once per element. Each iteration gets its own `constexpr` element, so `[: m :]` is legal inside the loop -- `m` really is a constant expression on every pass.

```
template for (constexpr auto m
              : std::define_static_array(
                  std::meta::nonstatic_data_members_of(^^T, ctx))) {
    std::println("  {} = {}",
                 std::meta::identifier_of(m),
                 obj.[: m :]);
}
```

That's the post-1 JSON serializer teaser, made real. No macros. No SFINAE. No external code generator. Just `^^` + `[: r :]` + `template for`, and the compiler writes the per-field code for you.

`break` / `continue` / `return` work like in a regular loop. With `if constexpr` inside, `continue` becomes tree-shaking: an annotated `skip` field generates no code at all.

This closes Arc 1 of the wro.cpp reflection series. Arc 2 (post 5 onward) puts the three primitives to work: enum-to-string without `magic_enum`, auto `std::formatter<T>`, derived equality / hash / ordering.

Read it: https://wrocpp.github.io/posts/template-for-expansion-statements/

What's the first compile-time loop you'd unroll? Drop it in the comments.

## Hashtags
#cpp #cpp26 #reflection #p1306 #p2996 #moderncpp #compiletime #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline "template for." with a blue period. Subtitle on the loop primitive of C++26 reflection -- combine ^^ and [: r :] with template for and the JSON serializer stops being a teaser.

## Suggested post time
Sunday 2026-05-03, 10:00 CET
Reason: matches the post's pubDate; Sunday morning is a calmer slot for in-depth technical reads.
