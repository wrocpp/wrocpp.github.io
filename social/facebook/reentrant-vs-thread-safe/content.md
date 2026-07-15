---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-07-31"}
# Thread-safe code can still deadlock itself
The Qt handler contract wanted reentrant, not just thread-safe. A std::mutex gives you the second without the first, and the difference can deadlock a signal handler.
:::

::::
