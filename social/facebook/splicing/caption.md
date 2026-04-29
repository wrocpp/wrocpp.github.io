# Splicing: [: r :] and putting reflections back into code

## Body
The piece that makes C++26 reflection composable.

`^^T` gives you a reflection. `[: r :]` gives the entity back -- a type, an expression, a member access. Together they round-trip the program: walk a struct's members, then write `obj.[:member:]` and let the compiler emit `obj.x`, `obj.y`, etc.

Part 3 of the wro.cpp reflection series. Builds the second half of the toolkit.

Read it: https://wrocpp.github.io/posts/splicing/

## Hashtags
#cpp #cpp26 #reflection #p2996 #moderncpp #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline "[: r :]." with the brackets in orange and a blue period. Subtitle on the splicer being the inverse of ^^.

## Suggested post time
Friday 2026-05-01, 10:00 CET
Reason: matches the post's pubDate; same slot as the LinkedIn post.
