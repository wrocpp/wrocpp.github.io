---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-26"}
# One adaptor turns a filter bug into a compile error
filter, reverse and as_rvalue over a vector of strings overflows the heap under AddressSanitizer on GCC 16.2. With views::as_input first, the reverse no longer compiles.
:::

::::
