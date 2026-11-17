# template for over a temporary tuple of constants fails on GCC 16.2 and clang trunk

## Body
Leonardo Rossi wrote a LinkedIn post about fold expressions in a Qt code base. It ends with C++26 features that replace an index_sequence lambda, and I ran them on 2026-11-17.

Fold grouping and pack indexing behave as described: (... - v) of 10, 3, 2 is 5 and (v - ...) is 9, and args...[2] returns the third argument on GCC 16.2 and Clang 22.1.

The trap is in template for. With a constexpr loop variable it compiles over a static constexpr tuple, and each element is a template argument. Over std::tuple{1uz, 2uz, 3uz} or a local constexpr tuple without static, GCC 16.2 and clang trunk reject it. The post quotes both errors.

A structured binding pack is the third way to walk the table, and it is accepted only inside a template. In the example the three ways give the same count for a table of three member-pointer pairs.

https://wrocpp.github.io/posts/template-for-constant-tuple-must-be-static/

## Hashtags
#cpp #cpp26 #templatefor #foldexpressions #packindexing #gcc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A static tuple works in template for. A temporary does not." with a subtitle about GCC 16.2, clang trunk and static constexpr. Citation footer: wro.cpp, 2026-12-23.

## Suggested post time
Wednesday 2026-12-23, 08:00 UTC
Reason: the morning slot on the publication day; this is the first of a pair, the second follows on 24 December.
