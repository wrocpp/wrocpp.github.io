# Catching a leftover std::function copy before it ships

## Body
Five stock clang-tidy checks stay silent on a std::function moved down a by-value chain, and a sixth warns about the corrected code. A short custom query check finds the three bad sites. ThreadSanitizer reports the wrong-thread destructor on libc++ only when the destructor touches thread-confined state.

https://wrocpp.github.io/posts/detect-the-leftover-copy/

## Hashtags
#cpp #cplusplus #clangtidy #threadsanitizer #libcxx #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Five stock clang-tidy checks miss the leftover copy" with a subtitle saying a custom query check finds the three bad moves and ThreadSanitizer needs a destructor that touches thread-confined state. Citation footer: wro.cpp, 2026-10-26.

## Suggested post time
Monday 2026-10-26, 16:00 UTC
Reason: second post of the day; the Boost modules post holds the 08:00 UTC slot.
