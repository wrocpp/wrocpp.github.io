# When a std::generator const& argument outlives the call, by compiler

## Body
Pass a temporary to a coroutine by const& and write the call in a range-for. It is safe on GCC 15.1 and Clang 19.1 or later, and it dangles on GCC 14.2 and MSVC 19.51. Store the generator first and it dangles on every compiler I ran. None of them warned.

https://wrocpp.github.io/posts/generator-const-reference-lifetime/

## Hashtags
#cpp #cpp23 #coroutines #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A generator's const& can dangle" with a subtitle about the range-for result on GCC, Clang and MSVC. Citation footer: wro.cpp, 2026-11-24.

## Suggested post time
Tuesday 2026-11-24, 16:00 UTC
Reason: the second slot of the day, beside the Meeting C++ program post.
