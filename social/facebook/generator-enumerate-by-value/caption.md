# What a by-value std::generator enumerate allocates on GCC and Clang

## Body
Alex Dathskovsky posted a std::generator enumerate that takes its container by value, which is the safe choice for a coroutine parameter. I counted what it allocates.

For a four-element array, GCC 16.2 makes one 144-byte allocation and Clang 23.1 makes none from -O1. A vector of 1000 ints adds a 4000-byte copy on both. std::views::enumerate allocates nothing.

https://wrocpp.github.io/posts/generator-enumerate-by-value/

## Hashtags
#cpp #cpp23 #coroutines #ranges #stdlib #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A by-value generator allocates 144 bytes on GCC" with a subtitle comparing GCC 16.2, Clang 23.1 and std::views::enumerate. Citation footer: wro.cpp, 2026-11-08.

## Suggested post time
Sunday 2026-11-08, 16:00 UTC
Reason: the second slot of the day.
