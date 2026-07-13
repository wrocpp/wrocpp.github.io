# std::pmr is one abstract class with three functions

## Body
Most allocator tutorials open with a wall of template parameters. std::pmr does not.

The whole framework sits on one class, std::pmr::memory_resource, with three functions to override. The demo writes one in a dozen lines that prints every allocation. A pmr::vector on top asks for 4, 8, 16, then 32 bytes as it grows. Put a monotonic_buffer_resource backed by stack memory in front, and those four heap requests become zero. The container never changes; only the resource behind it does.

pmr has been in the standard since C++17. Episode 1 of a new series.

https://wrocpp.github.io/posts/pmr-three-functions/

## Hashtags
#cpp #cplusplus #cpp17 #programming #performance

## Alt-text
A cream wro.cpp social card reading "The whole allocator zoo rests on one class", introducing std::pmr::memory_resource.

## Suggested post time
Wednesday 2026-07-22, 10:00 CET
Reason: midweek morning CET, shared with the LinkedIn post.
