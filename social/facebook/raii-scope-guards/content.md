---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-12"}
# The one scope guard that is allowed to throw
scope_exit and scope_fail have noexcept destructors, so a throwing action terminates. scope_success runs only on a normal exit, so its action may throw. Run on GCC 16.2.
:::

::::
