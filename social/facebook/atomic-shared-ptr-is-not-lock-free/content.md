---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-22"}
# Atomic shared_ptr is not lock-free
is_lock_free() is false on GCC 16.2, GCC trunk and MSVC. On GCC 16.2 a load takes a lock bit and 3 locked instructions, a plain copy 1. libc++ does not compile it.
:::

::::
