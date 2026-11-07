# When a std::generator const& argument outlives the call, by compiler

## Body
A coroutine that takes a const& and is called with a temporary is safe on some compilers and broken on others.

I ran one std::generator on ten configurations. With the temporary written in a range-for, it lives through the loop on GCC 15.1 and later and on Clang 19.1 and later. It is gone before the first resume on GCC 14.2 and on MSVC 19.51. If the generator is stored first, the temporary is gone on all ten.

No compiler warned about either call, up to -Weverything on Clang and /W4 /analyze on MSVC. A reflection check of under 50 lines flags the signature on GCC 16.2, but it misses string_view, span and pointer parameters.

The post has the tables, the AddressSanitizer results and a list of what I did not run. The Core Guidelines advice still holds: take the object by value.

https://wrocpp.github.io/posts/generator-const-reference-lifetime/

## Hashtags
#cpp #cpp23 #cpp26 #coroutines #lifetime #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A generator's const& can dangle" with a subtitle about the range-for result on GCC, Clang and MSVC. Citation footer: wro.cpp, 2026-11-24.

## Suggested post time
Tuesday 2026-11-24, 16:00 UTC
Reason: the second slot of the day, beside the Meeting C++ program post.
