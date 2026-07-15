---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-07-19"}
# The C++20 line that un-garbles your logs
std::cout tears across threads. Wrap it in std::osyncstream and each line buffers privately, then emits to the stream in one atomic block.
:::

::::
