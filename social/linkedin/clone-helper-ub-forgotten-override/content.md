---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-15"}
# A forgotten clone() override still prints the right area
The 2014 helper casts a Square to Tile, which is undefined. GCC 16.2 and Clang 22.1 print no warning. Only UBSan reports it.
:::

::::
