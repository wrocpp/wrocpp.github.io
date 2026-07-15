---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-09-18"}
# static std::mutex initializes itself, safely
A function-local static std::mutex is the classic fix, and C++11 magic statics make its own initialization thread-safe: constructed exactly once, even under a stampede.
:::

::::
