---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-28"}
# Move a const local and you copy 400 KB
On GCC 16.2 the const vector took 163 page faults per call, a plain return took none. Both compilers warn, with the text they give a harmless move. clang-tidy flags two shapes they miss.
:::

::::
