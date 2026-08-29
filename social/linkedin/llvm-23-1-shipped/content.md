---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-09-01"}
# One change does not announce itself
Clang 23.1 elides more dead stores than 22 did. Writes through an object whose lifetime has ended can disappear, with nothing said at build time.
:::

::::
