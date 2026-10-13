# Catching a leftover std::function copy before it ships

## Body
The Qt HarmonyOS bug never reads the task after moving it, so use-after-move checks have nothing to report. I ran five stock clang-tidy move and parameter checks on a small sample of the by-value chain. None reported it. A sixth, cppcoreguidelines-rvalue-reference-param-not-moved, warned about the corrected code.

A custom clang-tidy query check on moves of std::function reports exactly the three by-value sites in the sample and none of the fixed ones. ThreadSanitizer reports the wrong-thread destructor on libc++, but only when the destructor touches state that belongs to another thread.

The post also walks through the libc++ move constructor, linked to a pinned commit. It is the last of four episodes on QTBUG-151347.

https://wrocpp.github.io/posts/detect-the-leftover-copy/

## Hashtags
#cpp #cplusplus #clangtidy #threadsanitizer #libcxx #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Five stock clang-tidy checks miss the leftover copy" with a subtitle saying a custom query check finds the three bad moves and ThreadSanitizer needs a destructor that touches thread-confined state. Citation footer: wro.cpp, 2026-10-26.

## Suggested post time
Monday 2026-10-26, 16:00 UTC
Reason: second post of the day; the Boost modules post holds the 08:00 UTC slot.
