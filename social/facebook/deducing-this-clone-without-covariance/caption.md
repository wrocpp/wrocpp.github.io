# Deducing this gives clone() the derived type without covariance, friend or CRTP

## Body
Episode 2 of a series on clone() and smart pointers. One member function with an explicit object parameter, clone(this Self&& self), returns a unique_ptr of the caller's own type and moves from a non-const rvalue. On GCC 16.2 and Clang 22.1 it replaces the 2014 helper, its friend template and its CRTP base. Each class still overrides two hooks, and a forgotten override is still undefined.

https://wrocpp.github.io/posts/deducing-this-clone-without-covariance/

## Hashtags
#cpp #cpp23 #deducingthis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One clone() replaces the 2014 helper, friend and CRTP" with a subtitle about the explicit object parameter, rvalue moves and the forgotten override that is still undefined. Citation footer: wro.cpp, 2026-12-17.

## Suggested post time
Thursday 2026-12-17, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
