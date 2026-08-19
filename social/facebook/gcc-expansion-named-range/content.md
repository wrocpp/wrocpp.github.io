---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-10-21"}
# Naming a constant makes GCC doubt it
An expansion statement over a compile-time range compiles inline and fails when the identical expression is given a name. Clang accepts both. The workaround is to delete the name.
:::

::::
