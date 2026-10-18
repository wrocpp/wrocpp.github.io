# GCC's development branch accepts designated initializers for base classes

## Body
In June our Brno post had to leave one example commented out: a designated initializer that names a member of a base class, from P2287R6. No compiler accepted it. On 2026-10-18 GCC's development branch compiles it with -std=c++29.

The post has a demo that runs on GCC trunk and prints the three forms of the feature. GCC 16.1 and 16.2 in C++26 mode reject the plain form, and so does Clang trunk in -std=c++2d. Trunk in C++26 mode still rejects the plain form and accepts the other two with a warning.

It also lists the 8 C++29 items GCC's status page marks as available in GCC 17, read on the same day.

https://wrocpp.github.io/posts/gcc-17-base-class-designators/

## Hashtags
#cpp #cpp29 #gcc #cplusplus #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "GCC trunk compiles what we commented out in June" with a subtitle saying P2287R6 builds with -std=c++29 and GCC 16.1 and Clang trunk reject the plain form. Citation footer: wro.cpp, 2026-10-25.

## Suggested post time
Sunday 2026-10-25, 16:00 UTC
Reason: second post of the day; the GoogleTest post holds the 08:00 UTC slot.
