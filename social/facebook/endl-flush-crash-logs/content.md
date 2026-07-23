---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-14"}
# std::endl is a performance bug
std::endl is a newline plus a flush, and the flush is usually wasted. A flush-counting streambuf proves a newline flushes zero times and endl flushes every time.
:::

::::
