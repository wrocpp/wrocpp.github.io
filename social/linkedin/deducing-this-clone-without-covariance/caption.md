# Deducing this gives clone() the derived type without covariance, friend or CRTP

## Body
Episode 2 of a series on clone() and smart pointers.

One member function with an explicit object parameter, clone(this Self&& self), now does what the 2014 helper, its friend template and its CRTP base did. A square clones into a unique_ptr to Square, a Figure& bound to a square clones into a unique_ptr to Figure, and a non-const rvalue moves. That answers the question that closed the 2014 article.

Each class still overrides two private virtual hooks, one that copies and one that moves, because an explicit object member function cannot be virtual. The cast inside clone() is the 2014 cast, so a forgotten override is still undefined.

One side finding: hooks that return a covariant pointer crash every GCC from 13.1 to 16.2 that I ran when a constant expression stores the result in a base pointer. That is GCC PR126324, fixed on trunk. On 2026-11-09 the entry was still open, with no commit on a release branch. Hooks that return a unique_ptr avoid it. The design itself runs on GCC 16.2 and Clang 22.1.

https://wrocpp.github.io/posts/deducing-this-clone-without-covariance/

## Hashtags
#cpp #cpp23 #cpp26 #deducingthis #smartpointers #polymorphism #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One clone() replaces the 2014 helper, friend and CRTP" with a subtitle about the explicit object parameter, rvalue moves and the forgotten override that is still undefined. Citation footer: wro.cpp, 2026-12-17.

## Suggested post time
Thursday 2026-12-17, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
