---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-10-27"}
# The loop compiles and does nothing
Abseil made the iterator from insert stop at end() using two bytes of static data. Same types, same signatures, no warning. Code that walked from an insert result now visits nothing.
:::

::::
