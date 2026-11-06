---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-29"}
# Chunks keep the early exit and vectorize
Chunks of 16 or 32 bytes. With 32 and AVX2 flags GCC emits 12 instructions and Clang 13; at -O2 they are longer than the scalar loop. Counts only, no timing.
:::

::::
