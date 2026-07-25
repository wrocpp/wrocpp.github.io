# You can see the dependency chain without running anything

## Body
A benchmark tells you B is faster than A. It does not tell you why. Two things answer that without running the program: the assembly the compiler already generated, and a machine model to price it.

The demo has two functions adding the same floats. GCC unrolled the first one eight times, which looks like an optimization, but every one of those eight adds writes the same register and reads what the previous add produced. It is still one serial chain, so the loop runs at the latency of a single add no matter how many add units sit idle.

The four-accumulator version interleaves four independent chains and becomes issue-bound instead. You have to write it by hand, because floating-point addition is not associative and the compiler will not regroup your adds.

The third pane is llvm-mca, which prices the assembly against a CPU model with no execution at all.

Episode 4: https://wrocpp.github.io/posts/verification-asm-llvm-mca/

## Hashtags
#cpp #cplusplus #performance #optimization #programming

## Alt-text
A cream wro.cpp social card reading "Eight adds, one register, one slow loop", about assembly and llvm-mca.

## Suggested post time
Saturday 2026-08-22, 10:00 CET
Reason: weekend mid-morning for a longer performance read.
