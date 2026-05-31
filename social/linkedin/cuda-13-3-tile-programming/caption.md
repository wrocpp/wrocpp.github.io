# CUDA 13.3: tile programming in C++ without the boilerplate

## Body
NVIDIA CUDA 13.3 (May 26) adds C++ tile programming. Declarative tile abstractions replace manual shared memory, synchronization, and indexing. The compiler handles memory staging and index arithmetic; you describe the tile shape and the operation.

CompileIQ autotuning uses evolutionary algorithms to tune tile sizes and memory layout per kernel: up to 15% speedup on GEMM and attention kernels (the workhorses of ML inference). Up to 7x speedup in CCCL 3.3 search. ~20% improvement in cuSOLVER syevj.

Works on Hopper and all other supported architectures. If your codebase runs llama.cpp, vLLM, or custom inference, the attention-kernel gain is directly relevant.

https://wrocpp.github.io/posts/cuda-13-3-tile-programming/

## Hashtags
#cuda #gpu #cpp #cpp26 #nvidia #performance #ml #compileiq #wrocpp

## Alt-text
Editorial card: "CUDA 13.3: tile programming in C++". Declarative GPU kernels with CompileIQ autotuning.

## Suggested post time
Friday 2026-06-12, 10:00 CET
