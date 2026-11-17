---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-11"}
# A coroutine call costs one 80-byte allocation
In a toy on GCC 16.2, recursive fib(27) made 635,621 calls and 635,621 allocations. Plain recursion made none. At -O0, fib(22) crashed on the default stack.
:::

::::
