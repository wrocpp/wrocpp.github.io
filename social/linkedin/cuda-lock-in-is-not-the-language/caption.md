# The warp primitive ported fine

## Body
The standard argument about CUDA: you write kernels against Nvidia warp primitives layered under template machinery tuned for a particular warp width, which welds your source to Nvidia hardware, so porting means rewriting rather than recompiling.

The first half is accurate. The conclusion is not, and it is checkable.

Take a warp-level float reduction using __shfl_down_sync, the shape in every reduction tutorial and a lot of production code. Compile it with nvcc and you get two device views, because PTX and SASS are different programs: sixty lines of virtual registers become forty-five of real ones, with the warp width compiled in as a lane mask.

You can watch the instability directly. The same source at sm_80 and sm_90 picks different instructions. And CUDA 13.3 will not target Volta at all: nvcc fatal, unsupported gpu architecture sm_70. An architecture from 2017.

Then the part that surprised me. Compiler Explorer carries SCALE, a third-party toolchain that presents as nvcc and targets AMD. Hand it the identical file, unmodified:

  ds_swizzle_b32 v1, v1 offset:swizzle(REVERSE,32)
  v_add_f32_dpp  v1, v1, v1 row_shr:1 row_mask:0xf bank_mask:0xf

Not emulation. That is AMD's native cross-lane path, and the addition is fused into the cross-lane operation. Nvidia's own output needs SHFL.DOWN and then a separate FADD.

So the supposedly unportable primitive did not merely survive the port. It came out idiomatic on the other vendor's hardware, arguably tighter than the original.

The lock-in is real and it is not in the language. It is the toolchain nobody else can implement from a specification, the headers that stop the file being C++ another compiler can read, and a 2024 licence clause aimed at translation layers.

All of it reproducible: https://wrocpp.github.io/posts/cuda-lock-in-is-not-the-language/

## Hashtags
#cpp #cplusplus #cuda #gpu #hpc #portability

## Alt-text
A wro.cpp card reading "The warp primitive ported fine", about CUDA portability and lock-in.

## Suggested post time
Monday 2026-10-19, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
