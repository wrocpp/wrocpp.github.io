# Does custom allocation still pay off in 2026?

## Body
"Just use a pool allocator" was better advice in 2005 than it is today. Here is the honest 2026 version.

I ran one workload twice: build a 64-element vector, twenty thousand times, once on the default allocator and once on a monotonic_buffer_resource reset between rounds. The allocation counts are exact: 140,000 calls into the global allocator on the default path, zero on the arena.

What does removing those 140,000 calls buy on real hardware? Less than the folklore says. A 2026 re-run of Berger's classic study, on modern hardware against mimalloc, found per-class custom allocators bought about 2.3 percent and region allocators up to about 15 percent, down from the 44 percent the 2002 paper reported. Modern general allocators have absorbed most of the old win.

The exception is fragmentation. Once the heap was fragmented, the general allocator degraded by up to 2x while the region allocator was unaffected. That is why trading and game code still use arenas: for the tail, not a headline throughput number. An arena's worst case is close to its average case.

So a pmr arena still earns its place where you need predictable latency and no fragmentation. For raw throughput on a clean heap, mimalloc or jemalloc may already be within a few percent.

Episode 3 of the pmr series.

https://wrocpp.github.io/posts/pmr-benchmarks-2026/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #performance #benchmarks #memory #moderncpp

## Alt-text
A cream wro.cpp card reading "mimalloc quietly closed most of the gap", on custom allocation benchmarks in 2026.

## Suggested post time
Wednesday 2026-08-19, 10:00 CET
Reason: midweek morning CET; matches the series cadence.
