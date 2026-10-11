# Measuring how much false sharing costs a counter on Apple silicon

## Body
Eight threads, each incrementing its own atomic counter. With the counters packed side by side, one increment took 176 ns. With each counter padded to its own block it took 2.11 ns. That is the same loop on an Apple M2 Max with GCC 16.2.

The post measures write contention from the ground up. Counters packed, padded to the interference size, padded to 128 and to 64 bytes, one shared counter, thread_local, and a stack local variable merged at the end. Every cell is 11 runs with the median, minimum, maximum and coefficient of variation, and the machine, flags and load are listed beside the numbers.

Three things I did not expect. Padding to 64 bytes was not enough on this chip, which reports a 128-byte cache line. One shared counter cost as much as the packed layout. And a thread_local counter shared cache lines between threads on macOS with GCC 16.2, while it did not in a Linux aarch64 Docker VM on the same Mac.

One Mac that was not quiet, no x86-64 numbers, and a list of what was not tested. Compiler Explorer is used only for the layout and correctness check, never for timings.

https://wrocpp.github.io/posts/measuring-false-sharing-cost/

## Hashtags
#cpp #performance #concurrency #atomics #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Counters 8 bytes apart ran 83 times slower on eight threads" with a subtitle saying one atomic counter per thread on an Apple M2 Max with GCC 16.2 took 176 ns per increment packed and 2.11 ns padded, on one Mac with no x86-64 numbers. Citation footer: wro.cpp, 2026-11-15.

## Suggested post time
Sunday 2026-11-15, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day, the day after the struct layout post.
