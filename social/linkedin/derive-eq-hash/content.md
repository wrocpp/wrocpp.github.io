---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-09-21"}
# Stop writing std::hash by hand
C++20 defaulted == and <=>, but std::hash still needs a hand-written specialization. Reflection derives hashing and ordering from a struct's fields, with opt-out annotations.
:::

::::
