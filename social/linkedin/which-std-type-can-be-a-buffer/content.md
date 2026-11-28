---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2027-01-14"}
# A 72-byte buffer that comes out at 73 bytes
std::inplace_vector of bytes stores a counter and has alignment 1, so it cannot hold a pimpl's Impl. C++26 trivial unions run on GCC trunk only and need a complete type.
:::

::::
