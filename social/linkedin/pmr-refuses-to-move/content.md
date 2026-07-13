---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-09-16"}
# The allocator that refuses to move
Across different arenas, move assignment cannot steal the buffer, so it allocates and copies every element. An O(1) move becomes an O(n) copy.
:::

::::
