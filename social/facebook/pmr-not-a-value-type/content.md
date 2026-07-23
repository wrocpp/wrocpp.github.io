---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-30"}
# Your pmr::vector is not a value type
Copy construction does not copy the allocator. The copy silently falls back to the default heap, even though it compares equal to the original.
:::

::::
