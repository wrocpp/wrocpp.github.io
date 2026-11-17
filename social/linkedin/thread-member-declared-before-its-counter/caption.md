# A thread that starts before its counter exists

## Body
A class that declares its std::jthread before the members the thread uses has a bug at both ends of the object's life. At construction the thread runs before those members exist. At destruction they are gone before the thread has stopped.

ThreadSanitizer reports the construction race on GCC 16.2 and clang trunk, with exit code 66. At the destruction end it is silent for an atomic and reports a vector. -Wall -Wextra -Weffc++ on GCC and -Weverything on clang say nothing about the order, and neither does clang-tidy. The fix is to declare the thread last.

The case is Jelle Bakker's (C++ Doctor), from his ebook "25 C++ Cases That Will Humble You". The code in the post is my own, and I ran every number myself.

https://wrocpp.github.io/posts/thread-member-declared-before-its-counter/

## Hashtags
#cpp #cpp20 #jthread #threads #sanitizers #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "TSan flags a thread that starts before its counter" with a subtitle about a std::jthread member declared too early. Citation footer: wro.cpp, 2026-11-11.

## Suggested post time
Wednesday 2026-11-11, 16:00 UTC
Reason: the second slot of the day.
