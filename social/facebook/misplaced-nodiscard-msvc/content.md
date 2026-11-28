---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-02"}
# One keyword turns [[nodiscard]] off on MSVC
static [[nodiscard]] int f() compiles at /W4 with no diagnostic on four MSVC builds, and a discarded call goes unreported. GCC and Clang reject it. /we5240 makes it an error.
:::

::::
