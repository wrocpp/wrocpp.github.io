---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-25"}
# Three halves sum to 0 when accumulate starts at 0
accumulate takes its result type from the initial value, so 0.5 + 0.5 + 0.5 returns the int 0. fold_left returns 1.5. GCC 16.2 and Clang 22.1 did not warn. MSVC and clang-tidy did.
:::

::::
