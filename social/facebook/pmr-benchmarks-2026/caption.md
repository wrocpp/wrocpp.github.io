# Does custom allocation still pay off in 2026?

## Body
I ran one workload twice: build a small vector twenty thousand times, on the default allocator and on a pmr arena. The arena did zero heap allocations; the default path did 140,000.

But raw speed is another question. A 2026 re-run of Berger's classic study found modern allocators like mimalloc have absorbed most of the old custom-allocation advantage: a few percent on a clean heap, down from 44 percent in 2002. Where arenas still win clearly is fragmentation, where general allocators can degrade by 2x and arenas do not.

So the honest pitch is predictable latency and no fragmentation, not a blanket speedup.

Episode 3 of the pmr series.

https://wrocpp.github.io/posts/pmr-benchmarks-2026/

## Hashtags
#cpp #cplusplus #cpp17 #performance #programming
