# Pick / Omit / Partial in C++26

## Body
TypeScript's `Pick<User, "name" | "age">` translated to C++. `std::meta::define_aggregate` synthesises a new type from a list of `meta::info` member descriptors. Combine with `nonstatic_data_members_of` and you get Pick / Omit / Partial without writing the new type by hand.

Honest scope: type synthesis is experimental in clang-p2996 / GCC 16.1 today; the post is upfront about which pieces work now vs which need the next compiler bump.

Series post 16 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/define-aggregate/

## Hashtags
#cpp #cpp26 #reflection #typesynthesis #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Pick / Omit / Partial in C++26". Subhead: define_aggregate synthesises types from struct shape. Citation: wro.cpp 2026-06-07.

## Suggested post time
Sunday 2026-06-07, 10:00 CET
Reason: Sunday morning slot for EU C++ audience.
