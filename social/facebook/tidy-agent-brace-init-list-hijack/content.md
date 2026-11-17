---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-03"}
# A copy in braces became an array of 1
With a list constructor, Value{v} wraps v in a one-element array. A clang-tidy query check flags 2 of 2 such lines in the example. It misses Value{3} and vector&lt;int&gt;{3}.
:::

::::
