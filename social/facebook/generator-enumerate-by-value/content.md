---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-08"}
# A by-value generator allocates 144 bytes on GCC
Alex Dathskovsky's std::generator enumerate, counted on Compiler Explorer. Clang 23.1 allocates nothing from -O1, and std::views::enumerate allocates nothing at all.
:::

::::
