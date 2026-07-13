# A pmr::vector on a stack buffer never calls new

## Body
On a hot path, the cost of std::vector is not the arithmetic. It is the call into the global allocator every time the vector grows, and that call is where latency spikes hide.

std::pmr lets you pay for memory once and then run without touching the allocator. To prove it, I overrode the global operator new to count heap allocations, then filled a pmr::vector with ten thousand ints. The vector drew from a monotonic_buffer_resource backed by 256 KB on the stack, with null_memory_resource as its upstream, so any spill past the buffer would throw instead of quietly reaching the heap.

The count came back zero. Ten thousand push_backs, several reallocations as the vector doubled, and the global allocator was never called.

That is the arena pattern trading systems and game engines use: pre-own a slab, run the round from it, release, repeat. null_memory_resource upstream turns "should not allocate" into "cannot allocate", so a mis-sized buffer fails loudly in testing instead of costing you a latency spike in production. The container never changes. Only the resource behind it moves from the heap to the stack.

Episode 2 of the pmr series.

https://wrocpp.github.io/posts/pmr-zero-heap/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #performance #hft #memory #moderncpp

## Alt-text
A cream wro.cpp card reading "Point a vector at the stack; it never touches the heap", on a stack-backed pmr arena.

## Suggested post time
Wednesday 2026-08-05, 10:00 CET
Reason: midweek morning CET; matches the series cadence.
