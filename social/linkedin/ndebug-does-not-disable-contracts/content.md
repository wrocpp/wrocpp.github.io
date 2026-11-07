---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-11-16"}
# NDEBUG leaves contract checks running on GCC 16.2
With -fcontracts, -DNDEBUG deletes assert() but a false contract_assert still terminates. Only -fcontract-evaluation-semantic=ignore stops the evaluation.
:::

::::
