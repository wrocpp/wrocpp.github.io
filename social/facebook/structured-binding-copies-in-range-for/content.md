---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-10"}
# A copy does not protect the iterator
A range-for with auto [id, payload] copies each map element. Erase the current one in the body and it is still undefined.
:::

::::
