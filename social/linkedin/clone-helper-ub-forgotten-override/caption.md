# The 2014 clone() helper is undefined behaviour when a class forgets one override

## Body
Episode 1 of a series on clone() and smart pointers.

The clone helper from the 2014 CppCodeReviewers article by Filip Sajdak returns a unique_ptr of the object's own static type. It calls a protected virtual clone() and casts the result to T*. If a derived class forgets its override, the virtual call returns a base-class object and the cast is undefined.

I ran it on GCC 16.2 and Clang 22.1, as C++11 and as C++26, with -Wall -Wextra -Wpedantic. Neither printed a diagnostic. A plain -O2 build printed the right area and exited 0, and AddressSanitizer on GCC 16.2 reported nothing. UBSan reported the cast. A call to a virtual function that only the derived class has ended in SIGSEGV.

The article's tests compare the static type and the area, and a test of that kind would pass for the copy.

https://wrocpp.github.io/posts/clone-helper-ub-forgotten-override/

## Hashtags
#cpp #cpp11 #cpp26 #undefinedbehavior #ubsan #smartpointers #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A forgotten clone() override still prints the right area" with a subtitle about the 2014 helper, the missing compiler warning and UBSan. Citation footer: wro.cpp, 2026-12-15.

## Suggested post time
Tuesday 2026-12-15, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
