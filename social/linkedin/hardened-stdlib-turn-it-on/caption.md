# The hardened standard library turns an out-of-bounds read into a stop

## Body
vector::operator[] with an out-of-bounds index is undefined behavior. In practice it reads whatever is next in memory, hands it back as a valid int, and your program keeps running with a wrong answer until it crashes somewhere else entirely. at() throws, but nobody writes at() in a hot loop, so the checked path goes unused exactly where it would help.

The hardened standard library changes the default. Build with one macro and operator[] gains a bounds check that stops the program at the fault instead of reading garbage. For libstdc++ it is -D_GLIBCXX_ASSERTIONS. For libc++ it is -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_FAST. The checks cover operator[], span, string_view, and iterator ranges.

The instinct is that bounds checking is too slow for production. Measured, it usually is not: a predictable branch the CPU learns immediately, and many checks the compiler removes when it can prove the index is in range. Google has reported that deploying this class of hardening cut its production segfault rate by about a third with performance essentially unchanged.

Set it in your release build, not just debug. The bugs it catches are the ones that reach production: https://wrocpp.github.io/posts/hardened-stdlib-turn-it-on/

Is hardening on in your release builds today?

## Hashtags
#cpp #cplusplus #cpp26 #security #safety #stdlib #programming

## Alt-text
A cream wro.cpp social card reading "One flag turns a silent bug into a stop", about the hardened standard library adding a bounds check to vector operator[].

## Suggested post time
Saturday 2026-08-08, 10:00 CET
Reason: post lands on its pubDate; weekend mid-morning suits longer-read safety content.
