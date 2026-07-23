---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-22"}
# Your logger's real cost is on the hot path
osyncstream, mutex, and print all synchronize on the calling thread. The fastest loggers enqueue a raw record and format on a background thread instead.
:::

::::
