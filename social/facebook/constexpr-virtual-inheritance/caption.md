# Constexpr constructors with virtual bases work in GCC 16 and Clang trunk

## Body
GCC 16.1 and Clang trunk now accept a constexpr constructor in a class with a virtual base (P3533R2). GCC 15.3 and Clang 23.1 reject it. One virtual call through the base still fails on GCC 16, and the post shows the demo and a table of seven compiler versions.

https://wrocpp.github.io/posts/constexpr-virtual-inheritance/

## Hashtags
#cpp #cpp26 #constexpr #gcc #clang #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "GCC 16 compiles a constexpr constructor with a virtual base" with a subtitle saying Clang trunk does too and one virtual call through the base still fails on GCC 16. Citation footer: wro.cpp, 2026-10-30.

## Suggested post time
Friday 2026-10-30, 16:00 UTC
Reason: second post of the day; the P0963 post holds the 08:00 UTC slot.
