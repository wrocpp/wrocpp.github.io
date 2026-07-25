# The hottest line is often not the one worth optimizing

## Body
A sampling profiler shows where time is spent. That is not the question you have. You want to know where making things faster would make the program faster, and in a concurrent program the two come apart. A thread burning 40% of samples while blocked on a lock is not a 40% opportunity.

Coz attacks that with causal profiling. It cannot make one line faster, so it slows everything else down by a set amount, which is observationally the same thing. You get a graph, per line, of predicted whole-program speedup. A flat line means optimizing there is worthless however fast you make it.

Also worth knowing in 2026: perf with Hotspot on Linux, Tracy when the problem is the worst frame rather than the average, samply as the easy cross-platform on-ramp, and poop for honestly comparing two binaries.

Episode 5: https://wrocpp.github.io/posts/verification-profilers/

## Hashtags
#cpp #cplusplus #performance #profiling #programming

## Alt-text
A cream wro.cpp social card reading "The hottest line may be worth nothing", about causal profiling.

## Suggested post time
Monday 2026-08-24, 10:00 CET
Reason: Monday mid-morning CET for the EU audience.
