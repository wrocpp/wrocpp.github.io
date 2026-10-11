# Measuring how much false sharing costs a counter on Apple silicon

## Body
Eight threads, each incrementing its own atomic counter: 176 ns per increment when the counters sit side by side, 2.11 ns when each is padded to its own block. Apple M2 Max, GCC 16.2. The post also measures 64 and 128 byte padding, one shared counter and thread_local counters, with the machine and load listed. One Mac, no x86-64 numbers.

https://wrocpp.github.io/posts/measuring-false-sharing-cost/

## Hashtags
#cpp #performance #concurrency #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Counters 8 bytes apart ran 83 times slower on eight threads" with a subtitle saying one atomic counter per thread on an Apple M2 Max with GCC 16.2 took 176 ns per increment packed and 2.11 ns padded, on one Mac with no x86-64 numbers. Citation footer: wro.cpp, 2026-11-15.

## Suggested post time
Sunday 2026-11-15, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day, the day after the struct layout post.
