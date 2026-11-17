---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-07"}
# make_shared took 24 bytes, make_unique 4
A local shared_ptr that is only dereferenced. A tidy-agent check flags it and rewrites it, and it breaks one class that shares itself.
:::

::::
