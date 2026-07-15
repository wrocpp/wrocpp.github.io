---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-07-23"}
# std::print quietly fixed what iostreams never did
A single std::print call never interleaves with another, the printf-style atomicity iostreams never had. But split a line across two calls and it can still tear.
:::

::::
