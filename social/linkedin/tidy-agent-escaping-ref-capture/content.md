---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-08"}
# 6 of 9 dangling lambdas flagged, and 3 of 5 safe ones
The tidy-agent plugin check reports a by-reference lambda that is returned or stored. Clang 23.1 warns on 1 of the 9, or 4 with its lifetime flag. One case escapes every tool.
:::

::::
