# Constexpr constructors with virtual bases work in GCC 16 and Clang trunk

## Body
A class with a virtual base could not have a constexpr constructor until P3533R2. On 2026-10-18, GCC 16.1 and 16.2 accept it with -std=c++26, and Clang trunk accepts it. GCC 15.3, GCC 14.1 and Clang 23.1 reject it.

One case differs. A virtual call through a reference to the virtual base inside a constant expression fails on GCC 16 with a specific message, and Clang trunk runs it. I did not determine whether the standard requires that case, so the post reports behavior and not a bug.

Both cases are Compiler Explorer demos on two compilers each, with the full table of seven compiler versions.

https://wrocpp.github.io/posts/constexpr-virtual-inheritance/

## Hashtags
#cpp #cpp26 #constexpr #gcc #clang #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "GCC 16 compiles a constexpr constructor with a virtual base" with a subtitle saying Clang trunk does too and one virtual call through the base still fails on GCC 16. Citation footer: wro.cpp, 2026-10-30.

## Suggested post time
Friday 2026-10-30, 16:00 UTC
Reason: second post of the day; the P0963 post holds the 08:00 UTC slot.
