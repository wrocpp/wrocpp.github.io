---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-08-08"}
# Same cast, two compilers, two answers
Converting an out-of-range double to int is undefined. GCC gives -2147483648, Clang gives 0, and GCC will not even check unless you name the flag.
:::

::::
