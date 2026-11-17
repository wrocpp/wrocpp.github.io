# An empty constructor written {} stops {} from zeroing the object

## Body
span() = default and span() {} look like the same empty constructor. They are not.

After Daniel Lemire's post of 2 November on the speed cost, I checked the semantics. With the constructor defaulted in the class, T() and T{} read as zero and the class is trivial. With {}, or with = default written outside the class, neither zeroes the members and the class is not trivial. That held on GCC 16.2, GCC trunk and Clang 22.1, decided in constant expressions.

Reading an unset local printed 0 on GCC 16.2 in C++26 mode, where it is erroneous behaviour. With C++23 the defaulted class printed -104, and Clang's MemorySanitizer reported the read. An object from new is still indeterminate in C++26.

My default is a default member initialiser on every member, and = default in the class. I did not run timings.

https://wrocpp.github.io/posts/default-or-braces-constructor-initialisation/

## Hashtags
#cpp #cpp26 #constructors #initialization #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Writing {} instead of = default stops T{} zeroing" with a subtitle about the trivial type and GCC 16.2 and Clang 22.1. Citation footer: wro.cpp, 2026-11-24.

## Suggested post time
Tuesday 2026-11-24, 08:00 UTC
Reason: the morning slot on the publication day.
