# A pmr::vector on a stack buffer never calls new

## Body
On a hot path, the cost of std::vector is the call into the global allocator each time it grows. std::pmr lets you pay for memory once and skip that.

I overrode operator new to count heap allocations, then filled a pmr::vector with ten thousand ints from a monotonic_buffer_resource backed by 256 KB of stack. The count came back zero. Every byte came from the buffer, and null_memory_resource upstream meant any spill would have thrown rather than reaching the heap.

That is the per-frame arena game engines and trading systems rely on. The container never changes; only the resource behind it does.

Episode 2 of the pmr series.

https://wrocpp.github.io/posts/pmr-zero-heap/

## Hashtags
#cpp #cplusplus #cpp17 #performance #programming
