# Google Benchmark runs live on Compiler Explorer

## Body
You do not need a local build to run a real microbenchmark. Add the benchmark library on Compiler Explorer, turn on execution, and Google Benchmark prints its timing table in the browser.

The demo is also the first lesson every benchmark teaches. Two loops call std::sqrt. One throws the result away, so the optimizer deletes the loop and reports 0 ns over a trillion iterations. The other uses benchmark::DoNotOptimize, which forces the compiler to keep the work, and now the timing is honest. A benchmark that does not consume its result is measuring nothing.

Runnable demo: https://wrocpp.github.io/posts/google-benchmark-on-ce/

## Hashtags
#cpp #cplusplus #performance #benchmarking #programming

## Alt-text
A cream wro.cpp social card reading "Your benchmark measured an empty loop", about benchmark::DoNotOptimize on Compiler Explorer.

## Suggested post time
Monday 2026-07-27, 10:00 CET
Reason: Monday mid-morning CET for the EU audience.
