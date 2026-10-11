# Measuring what false sharing costs a counter on three machines

## Body
Eight threads, each incrementing its own atomic counter: 176 ns per increment when the counters sit side by side, 2.11 ns when each is padded to its own block. That is 83 times on an Apple M2 Max with GCC 16.2, 88 times in a Linux aarch64 Docker VM, and 13.5 times on an x86-64 laptop CPU with hyperthread pairs. The post also measures 64 and 128 byte padding, one shared counter and thread_local counters, with each machine and its load listed.

https://wrocpp.github.io/posts/measuring-false-sharing-cost/

## Hashtags
#cpp #performance #concurrency #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Counters 8 bytes apart ran 13 to 88 times slower on eight threads" with a subtitle saying one atomic counter per thread, packed against padded to the interference size, ran 13.5 times slower on an x86-64 laptop CPU using hyperthread pairs, 83 times on an Apple M2 Max and 88 times in a Linux aarch64 VM, on three machines with clocks not fixed. Citation footer: wro.cpp, 2026-11-15.

## Suggested post time
Sunday 2026-11-15, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day, the day after the struct layout post.
