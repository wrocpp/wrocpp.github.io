# An empty constructor written {} stops {} from zeroing the object

## Body
After Daniel Lemire's post on = default against {}, I checked what each spelling does. With the constructor defaulted in the class, T{} zeroes the members and the class stays trivial. With {}, neither is true. That held on GCC 16.2 and Clang 22.1. A read of an unset local printed 0 on GCC 16.2 in C++26 mode, and Clang's MemorySanitizer reported it.

https://wrocpp.github.io/posts/default-or-braces-constructor-initialisation/

## Hashtags
#cpp #cpp26 #constructors #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Writing {} instead of = default stops T{} zeroing" with a subtitle about the trivial type and GCC 16.2 and Clang 22.1. Citation footer: wro.cpp, 2026-11-24.

## Suggested post time
Tuesday 2026-11-24, 08:00 UTC
Reason: the morning slot on the publication day.
