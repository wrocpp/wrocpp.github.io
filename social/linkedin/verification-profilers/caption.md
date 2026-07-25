# The hottest line is often not the one worth optimizing

## Body
A sampling profiler interrupts your program many times a second and records the stack. Aggregate that and you get where time is spent. It is the right first tool and often enough.

But "where time is spent" is not the question you have. You want to know where making things faster would make the program faster, and in a concurrent program those two come apart badly. A thread burning 40% of samples while blocked behind a lock is not a 40% opportunity. Speed up a function that is not on the critical path and nothing changes. Optimize the hottest line, measure, win nothing: everyone who has profiled a threaded program has had that afternoon.

Coz attacks the gap with causal profiling. It cannot make a line faster to see what would happen, so it slows down everything else by a set amount, which is observationally equivalent. The result is a graph, per line, of predicted whole-program speedup against hypothetical local speedup. A flat line means optimizing there is worthless no matter how much faster you make it.

The rest of the toolbox worth knowing in 2026: perf with Hotspot as the Linux baseline, Tracy when the problem is the 1% frame rather than the average, samply as the low-friction cross-platform on-ramp, and poop for honestly comparing two binaries with confidence intervals.

The habit worth taking: when a profiler says a line is hot, treat it as a hypothesis, not an instruction. Ask what would happen if that line were free. Sometimes the answer is nothing, and knowing that before you spend a week is the value of the tool.

Episode 5: https://wrocpp.github.io/posts/verification-profilers/

Which profiler do you actually reach for?

## Hashtags
#cpp #cplusplus #performance #profiling #optimization #programming

## Alt-text
A cream wro.cpp social card reading "The hottest line may be worth nothing", about causal profiling and the 2026 profiler landscape.

## Suggested post time
Monday 2026-08-24, 10:00 CET
Reason: Monday mid-morning CET to open the week for the EU audience.
