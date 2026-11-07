# co_yield inside template for does not compile on GCC 16.2 or trunk

## Body
A std::generator over a struct's members, written as co_yield inside template for, stops the build on GCC 16.2 and on trunk. Reflecting the members into an array first and folding over an index_sequence builds and runs on both, with one allocation for a three-member struct.

https://wrocpp.github.io/posts/co-yield-inside-template-for/

## Hashtags
#cpp #cpp26 #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "co_yield in a template for fails on GCC 16.2" with a subtitle about the constexpr array and index_sequence fold that builds. Citation footer: wro.cpp, 2026-11-25.

## Suggested post time
Wednesday 2026-11-25, 08:00 UTC
Reason: the morning slot, one day after the generator lifetime post it follows.
