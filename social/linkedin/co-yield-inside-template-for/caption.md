# co_yield inside template for does not compile on GCC 16.2 or trunk

## Body
The obvious generator over a struct's members puts co_yield inside template for. On Compiler Explorer, GCC 16.2 and GCC trunk both stop the build with -std=c++26 -freflection.

What builds is to reflect the members into a constexpr array outside the coroutine and fold over an index_sequence inside it. A three-member struct costs one 448-byte allocation. A nested struct, with one helper coroutine per member, costs 11 allocations and 3104 bytes for six fields.

At -O2 with -Werror, both compilers stop on a mismatched-new-delete warning inside <generator>. I do not know why, and the post says so.

Everything here is GCC only, because Clang trunk on Compiler Explorer has no std::meta.

https://wrocpp.github.io/posts/co-yield-inside-template-for/

## Hashtags
#cpp #cpp26 #reflection #coroutines #gcc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "co_yield in a template for fails on GCC 16.2" with a subtitle about the constexpr array and index_sequence fold that builds. Citation footer: wro.cpp, 2026-11-25.

## Suggested post time
Wednesday 2026-11-25, 08:00 UTC
Reason: the morning slot, one day after the generator lifetime post it follows.
