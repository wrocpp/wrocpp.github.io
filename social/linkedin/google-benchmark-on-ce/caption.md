# Google Benchmark runs live on Compiler Explorer

## Body
Google Benchmark is a Compiler Explorer library. Add it from the libraries panel, turn on execution, and BENCHMARK_MAIN() runs on CE's servers and prints the timing table back to you. No local checkout, no CMake, no linking to figure out.

The demo doubles as the first lesson every microbenchmark teaches the hard way. Two loops call std::sqrt. One throws the result away, so the optimizer deletes the whole loop body and Benchmark reports 0.000 ns over a trillion iterations, a number that looks precise and means nothing. The other passes the result through benchmark::DoNotOptimize, which forces the compiler to keep the computation, and now you get an honest sub-nanosecond timing.

DoNotOptimize is an inline-assembly barrier that costs zero instructions and tells the compiler the value is observed. Its sibling ClobberMemory does the same for stores. The rule that falls out: a microbenchmark that does not consume its result is measuring nothing, and the giveaway is a suspiciously round time over an astronomical iteration count.

Runnable demo, with the DEBUG-build caveat spelled out: https://wrocpp.github.io/posts/google-benchmark-on-ce/

What is the most misleading benchmark number you have been burned by?

## Hashtags
#cpp #cplusplus #performance #benchmarking #optimization #compilerexplorer #programming

## Alt-text
A cream wro.cpp social card reading "Your benchmark measured an empty loop", about benchmark::DoNotOptimize and Google Benchmark on Compiler Explorer.

## Suggested post time
Monday 2026-07-27, 10:00 CET
Reason: Monday mid-morning CET catches the EU audience at the start of the week.
