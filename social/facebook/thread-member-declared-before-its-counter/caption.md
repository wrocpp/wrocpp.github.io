# A thread that starts before its counter exists

## Body
A std::jthread member declared before the data it uses starts running before that data exists, and at destruction the data is gone before the thread stops.

ThreadSanitizer reports the construction race on GCC 16.2 and clang trunk. The compiler warnings I tried say nothing about the order. The fix is to declare the thread last. The case is Jelle Bakker's (C++ Doctor).

https://wrocpp.github.io/posts/thread-member-declared-before-its-counter/

## Hashtags
#cpp #cpp20 #jthread #threads #sanitizers #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "TSan flags a thread that starts before its counter" with a subtitle about a std::jthread member declared too early. Citation footer: wro.cpp, 2026-11-11.

## Suggested post time
Wednesday 2026-11-11, 16:00 UTC
Reason: the second slot of the day.
