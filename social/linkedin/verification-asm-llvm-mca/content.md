---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-27"}
# Eight adds, one register, one slow loop
GCC unrolled the loop eight times and it changed nothing: every add still writes xmm0. The assembly shows the dependency chain, and llvm-mca prices it.
:::

::::
