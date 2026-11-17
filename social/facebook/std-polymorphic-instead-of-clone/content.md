---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-21"}
# Copy a polymorphic object without writing clone()
std::polymorphic copies the dynamic type, so there is no override to forget. A row of three copies with 4 allocations, as with unique_ptr and clone(). libc++ trunk did not define it.
:::

::::
