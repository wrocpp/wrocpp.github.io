---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-11"}
# TSan flags a thread that starts before its counter
A std::jthread member declared before the data it uses breaks at both ends of the object's life. GCC and clang warnings say nothing about the order.
:::

::::
