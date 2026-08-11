---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-19"}
# A dangling warning with nothing to dangle
clang lifetimebound has no conditional form, so a value_or returning a copy still trips -Wdangling. The code is correct and the warning is not.
:::

::::
