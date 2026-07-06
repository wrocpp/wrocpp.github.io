# Splicing: [: r :] and putting reflections back into code

## Body
Reflection in C++26 has two halves.

The first, `^^T`, takes an entity and returns a `std::meta::info`, the post-2 territory. The second, the splicer `[: r :]`, takes a reflection and gives the entity back: a type, an expression, a member access, a template argument, anywhere the original name would fit.

This is the piece that makes reflection composable. Without splicing you can inspect a struct's members all you want, but you can't write code that reads `obj.field` for an arbitrary `field`. With splicing:

```
obj.[:member:]      // member access
[:type_of(m):]      // type position
fn<[:r:]>()         // template argument
typename [:t:]      // disambiguator
```

Where `^^` walks types into reflections, `[: r :]` walks reflections back into source. Together they round-trip the program.

This is part 3 of the wro.cpp reflection series. Posts 2 + 3 give you the two halves; post 4 (template for) adds the loop primitive and the post-1 JSON-serializer teaser stops being a teaser.

Read it: https://wrocpp.github.io/posts/splicing/

What's the first piece of code you'd splice? Drop it in the comments.

## Hashtags
#cpp #cpp26 #reflection #p2996 #moderncpp #compiletime #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline "[: r :]." with the brackets in orange and the period in blue. Subtitle on the splicer being the inverse of ^^ -- the piece that makes reflection composable.

## Suggested post time
Friday 2026-05-01, 10:00 CET
Reason: matches the post's pubDate; Friday morning catches European C++ engineers wrapping up the week.
