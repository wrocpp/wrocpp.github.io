# The hardened standard library turns an out-of-bounds read into a stop

## Body
vector::operator[] with a bad index is undefined behavior. It reads whatever is next in memory, returns it as a valid int, and your program runs on with a wrong answer until it crashes somewhere unrelated. at() throws, but nobody writes at() in a hot loop.

The hardened standard library changes the default. Build with one macro and operator[] gains a bounds check that stops at the fault instead of reading garbage: -D_GLIBCXX_ASSERTIONS for libstdc++, _LIBCPP_HARDENING_MODE for libc++. It is fast enough for production, and Google has reported it cut their segfault rate by about a third.

Turn it on in release builds: https://wrocpp.github.io/posts/hardened-stdlib-turn-it-on/

## Hashtags
#cpp #cplusplus #security #safety #programming

## Alt-text
A cream wro.cpp social card reading "One flag turns a silent bug into a stop", about the hardened standard library.

## Suggested post time
Saturday 2026-08-08, 10:00 CET
Reason: weekend mid-morning for longer-read safety content.
