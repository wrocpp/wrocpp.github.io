# template for: iterating reflections at compile time

## Body
Three primitives carry the whole C++26 reflection toolkit:

- `^^T` reflects an entity into a `std::meta::info`.
- `[: r :]` splices a reflection back into source.
- `template for` unrolls a loop at compile time, instantiating the body once per iteration with each value as a separate `constexpr`.

Together they form the post-1 JSON serializer teaser -- not as a clever hack, but as the natural composition:

```
template for (constexpr auto m
              : std::define_static_array(
                  std::meta::nonstatic_data_members_of(^^T, ctx))) {
    append_quoted(out, std::meta::identifier_of(m));
    out += ':';
    append_value(out, obj.[:m:]);
}
```

The compiler emits one block per field. There's no template recursion, no SFINAE, no fold expression hidden in a helper -- just a loop the compiler runs at compile time.

This is part 4 of the wro.cpp reflection series and the last of the foundational primitives. From here we build on top: <PostLink slug="enum-to-string">enum-to-string</PostLink>, <PostLink slug="auto-formatter">an auto formatter</PostLink>, <PostLink slug="derive-eq-hash">derived equality + hash</PostLink>, and the rest of the series.

Read it: https://wrocpp.github.io/posts/template-for-expansion-statements/

What's the first thing you'd unroll over a struct's members? Drop it in the comments.

## Hashtags
#cpp #cpp26 #reflection #p2996 #moderncpp #compiletime #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline "template for." in Quicksand with a blue period. Subtitle on combining ^^, [: r :], and template for to make the post-1 JSON serializer teaser stop being a teaser.

## Suggested post time
Sunday 2026-05-03, 10:00 CET
Reason: matches the post's pubDate; Sunday morning leans on the weekend technical-reading audience.
