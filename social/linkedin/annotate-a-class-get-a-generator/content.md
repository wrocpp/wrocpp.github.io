---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-29"}
# Reflection cannot write your coroutine
Annotations skip or rename a member and run steps lazily. A wrapper around a vector-returning method still builds 1000 elements for 3 consumed, against 7 as a coroutine.
:::

::::
