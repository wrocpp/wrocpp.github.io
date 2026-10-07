---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-02"}
# The same bad index: a compile error, then exit 0
static_assert stops the build on UB. With a run-time index at -O2, the same call printed stale memory.
:::

::::
