---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-06-18"}
# std::rotate: libstdc++ and libc++ disagree
Raymond Chen's June series shows the same call runs different algorithms in libstdc++ and libc++. n-1 swaps with good locality vs ~n/2 swaps with terrible locality. Which wins depends on your input shape.
:::

::::
