---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-15"}
# Counters 8 bytes apart ran 13 to 88 times slower on eight threads
One atomic counter per thread, packed against padded: 13.5 on an x86-64 laptop CPU (hyperthread pairs), 83 on an Apple M2 Max, 88 in a Linux aarch64 VM. Three machines, clocks not fixed.
:::

::::
