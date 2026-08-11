---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-10-12"}
# priority_queue will not let go of your object
top() returns a const reference, so a move-only element cannot be taken out at all. The fix is a const_cast followed immediately by pop, and the order matters.
:::

::::
