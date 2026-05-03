---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-05-12"}
# Is std::vector consteval, or constexpr?
Short answer: it has been constexpr-friendly since C++20. The intuition that vector "is consteval" is operationally right -- its values can only exist during constant evaluation.
:::

::::
