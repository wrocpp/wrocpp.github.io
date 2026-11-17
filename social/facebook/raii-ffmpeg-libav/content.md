---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-13"}
# One missed free leaked 33 allocations
On FFmpeg 9.0.2 an early exit that forgot the codec context leaked 64,720 bytes. unique_ptr wrappers cost one pointer each and leaked nothing on any path.
:::

::::
