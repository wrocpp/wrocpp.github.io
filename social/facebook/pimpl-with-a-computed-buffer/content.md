---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2027-01-13"}
# One pimpl, 72 bytes on one library, 56 on another
An inline buffer saves the pimpl an allocation per object and per copy. Its header needs a size it cannot see: check it with a C++26 static_assert message, or let reflection generate it.
:::

::::
