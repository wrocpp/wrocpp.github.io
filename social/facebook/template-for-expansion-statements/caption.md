# template for: iterating reflections at compile time

## Body
The loop primitive that makes C++26 reflection complete.

`^^T` gives you a reflection. `[: r :]` puts it back into code. `template for` (P1306) unrolls a loop at compile time, instantiating the body once per element, with `[: m :]` legal on every pass because `m` is genuinely constexpr per iteration.

The post-1 JSON serializer teaser stops being a teaser: one loop, N specialisations, zero macros.

Part 4 of the wro.cpp reflection series. Closes Arc 1.

Read it: https://wrocpp.github.io/posts/template-for-expansion-statements/

## Hashtags
#cpp #cpp26 #reflection #p1306 #p2996 #moderncpp #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline "template for." with a blue period. Subtitle on the loop primitive of C++26 reflection.

## Suggested post time
Sunday 2026-05-03, 10:00 CET
Reason: matches the post's pubDate; same slot as the LinkedIn post.
