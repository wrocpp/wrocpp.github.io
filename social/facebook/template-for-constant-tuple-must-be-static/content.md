---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-23"}
# A static tuple works in template for. A temporary does not.
GCC 16.2 and clang trunk reject a constexpr loop variable over std::tuple{1uz, 2uz, 3uz}. With static constexpr on the tuple, each element is a template argument.
:::

::::
