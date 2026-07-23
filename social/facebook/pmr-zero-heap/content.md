---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-26"}
# Point a vector at the stack; it never touches the heap
Override new to count heap calls, then fill a pmr::vector from a monotonic_buffer_resource on a stack buffer. Ten thousand pushes, zero heap allocations.
:::

::::
