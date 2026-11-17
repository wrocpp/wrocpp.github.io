---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-24"}
# Writing {} instead of = default stops T{} zeroing
With the constructor defaulted in the class, T{} zeroes the members and the type stays trivial. With {} neither holds. Checked on GCC 16.2 and Clang 22.1.
:::

::::
