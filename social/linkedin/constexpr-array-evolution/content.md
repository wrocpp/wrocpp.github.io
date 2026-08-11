---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-10-04"}
# Sorting at compile time waited for C++20
std::array's members became constexpr in C++17, but std::sort did not until C++20. That gap is why old lookup-table code hand-rolls its own sorting.
:::

::::
