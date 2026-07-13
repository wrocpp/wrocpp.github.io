# std::pmr is one abstract class with three functions

## Body
Most allocator tutorials open with a wall of template parameters. std::pmr does not.

The entire polymorphic memory resource framework (the arenas, the pool allocators, every pmr::vector and pmr::string) sits on one abstract class: std::pmr::memory_resource. You override three functions. do_allocate hands back bytes, do_deallocate takes them back, and do_is_equal says whether another resource can free your memory.

The demo writes such a resource in a dozen lines. It forwards to an upstream and prints every request. A pmr::vector on top of it asks for 4, 8, 16, then 32 bytes as it doubles, so four heap allocations, each printed. Then the same logger goes behind a monotonic_buffer_resource backed by 512 bytes on the stack. The vector takes its memory from the arena, the upstream logger is never called, and four heap requests become zero.

The mechanism is simple. Because the allocator is chosen at runtime behind one virtual call, resources stack: a pool in front of an arena in front of the heap is three objects wired by pointer. pmr has been in the standard since C++17.

Episode 1 of a new series on std::pmr.

https://wrocpp.github.io/posts/pmr-three-functions/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #allocators #memory #performance #moderncpp

## Alt-text
A cream wro.cpp social card reading "The whole allocator zoo rests on one class", introducing std::pmr::memory_resource.

## Suggested post time
Wednesday 2026-07-22, 10:00 CET
Reason: midweek morning CET for working-hours reach; matches the series cadence.
