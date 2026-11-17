---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-02"}
# 30 seconds became 30 milliseconds
A TTL in seconds stored in a field named timeoutMs compiles and runs 1000 times too short. A clang-tidy query check flags 2 of 2 such fields in the example. It cannot see a unit in a comment.
:::

::::
