# You can see the dependency chain without running anything

## Body
A benchmark tells you version B is faster than version A. It does not tell you why, and it cannot tell you what the ceiling is. Two things answer that without running the program: read the assembly the compiler already generated, then let a machine model price it.

The demo is two functions adding the same n floats. One uses a single accumulator, the other keeps four.

Look at the first one's inner loop. GCC unrolled it eight times, which looks like an optimization:

  vaddss xmm0, xmm0, DWORD PTR [rax]
  vaddss xmm0, xmm0, DWORD PTR [rax-28]
  vaddss xmm0, xmm0, DWORD PTR [rax-24]
  ...

Every one of those eight adds writes xmm0 and reads the xmm0 the previous add produced. Unrolling changed the loop overhead and nothing else. The adds are still a single serial chain, so the loop runs at the latency of one add per element no matter how many add units sit idle.

The four-accumulator version interleaves xmm0 through xmm3: four independent chains, nothing waiting on anything, bound by issue rate rather than latency. You had to write it by hand because floating-point addition is not associative, so the compiler will unroll (order preserved) but will not regroup.

The third pane is llvm-mca, which simulates the assembly against a CPU model and reports IPC, dispatch width, port pressure, and per-instruction latency. A number instead of an intuition, with no execution at all.

Episode 4: https://wrocpp.github.io/posts/verification-asm-llvm-mca/

How often do you actually read the generated assembly?

## Hashtags
#cpp #cplusplus #performance #optimization #assembly #compilerexplorer

## Alt-text
A cream wro.cpp social card reading "Eight adds, one register, one slow loop", about reading assembly and llvm-mca.

## Suggested post time
Saturday 2026-08-22, 10:00 CET
Reason: weekend mid-morning suits a longer performance read.
