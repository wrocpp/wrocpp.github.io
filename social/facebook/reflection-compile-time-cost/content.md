---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-05-29"}
# The hidden cost of `<meta>`: the three-line fix
The reflection header adds ~181ms per TU. The reflection algorithm costs ~0.07ms per enumerator. A three-line CMake PCH stanza cuts the header cost by 2.3x.
:::

::::
