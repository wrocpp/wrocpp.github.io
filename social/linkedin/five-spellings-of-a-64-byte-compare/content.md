---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-25"}
# A 64-byte compare loop stays scalar on Clang and MSVC
Array equality, memcmp and std::equal gave the same instructions as each other in all ten builds. GCC vectorizes the early-exit loop only with AVX2 flags.
:::

::::
