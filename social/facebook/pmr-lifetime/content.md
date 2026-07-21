---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-26"}
# The resource that died too soon
A pmr container frees memory back into its resource when destroyed, so the resource must outlive it. Get the declaration order wrong and it is undefined behavior.
:::

::::
