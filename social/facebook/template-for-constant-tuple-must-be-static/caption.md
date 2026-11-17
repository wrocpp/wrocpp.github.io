# template for over a temporary tuple of constants fails on GCC 16.2 and clang trunk

## Body
Building on a LinkedIn post by Leonardo Rossi about fold expressions. A template for loop with a constexpr loop variable compiles over a static constexpr tuple and is rejected over std::tuple{1uz, 2uz, 3uz} or a local constexpr tuple, on GCC 16.2 and clang trunk. Fold grouping, pack indexing and a structured binding pack are in the post too.

https://wrocpp.github.io/posts/template-for-constant-tuple-must-be-static/

## Hashtags
#cpp #cpp26 #templatefor #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A static tuple works in template for. A temporary does not." with a subtitle about GCC 16.2, clang trunk and static constexpr. Citation footer: wro.cpp, 2026-12-23.

## Suggested post time
Wednesday 2026-12-23, 08:00 UTC
Reason: the morning slot on the publication day; this is the first of a pair, the second follows on 24 December.
