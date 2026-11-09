# The 2014 clone() helper is undefined behaviour when a class forgets one override

## Body
Episode 1 of a series on clone() and smart pointers. The clone helper from the 2014 CppCodeReviewers article by Filip Sajdak casts the result of a virtual call to the derived type. If a derived class forgets its override, that cast is undefined. GCC 16.2 and Clang 22.1 printed no warning, and a plain -O2 build printed the right area. UBSan reported it.

https://wrocpp.github.io/posts/clone-helper-ub-forgotten-override/

## Hashtags
#cpp #cpp11 #ubsan #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A forgotten clone() override still prints the right area" with a subtitle about the 2014 helper, the missing compiler warning and UBSan. Citation footer: wro.cpp, 2026-12-15.

## Suggested post time
Tuesday 2026-12-15, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
