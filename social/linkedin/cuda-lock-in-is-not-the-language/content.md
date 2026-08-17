---
template: social/linkedin-post
---

::::post{type=insight theme=dark logo=top-left}

:::insight{citation="wro.cpp -- 2026-10-19"}
# The warp primitive ported fine
SCALE compiled an unmodified CUDA reduction for an AMD GPU. shfl_down_sync came out as ds_swizzle and v_add_f32_dpp, with the add fused in. The lock-in is the toolchain and the licence.
:::

::::
