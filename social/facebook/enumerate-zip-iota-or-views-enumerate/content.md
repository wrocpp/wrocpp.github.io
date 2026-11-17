---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-12-26"}
# A zip-based enumerate has no size and no common end
Over a vector, zip(iota, r) is neither sized nor common. ranges::to takes 2000 iterator steps against 1000 for views::enumerate. A bounded iota fixes both.
:::

::::
