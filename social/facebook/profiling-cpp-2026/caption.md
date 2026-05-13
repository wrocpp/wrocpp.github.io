# Profiling C++ in 2026

## Body
You'll use three or four profilers, not one: perf for "where is my time going" (system-wide sampling, ~1% overhead), Tracy for frame-aware tick loops, Perfetto for multi-process trace, Callgrind for cycle-exact diagnosis. Today's wro.cpp Toolset launch (MR5, first entry in the performance cluster) covers the decision tree end-to-end.

The interesting part: C++26 reflection eliminates manual `ZoneScoped` / `TRACE_EVENT` per method. P3394 annotation `[[=trace]]` per field auto-instruments the interface; reflection walks members, wraps annotated ones, leaves the rest. Same harness across Tracy / Perfetto / OpenTelemetry -- only the sink changes.

https://wrocpp.github.io/toolset/profiling-cpp-2026/

## Hashtags
#cpp #cpp26 #profiling #performance #reflection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Profiling C++ in 2026". Subhead: perf / Tracy / Perfetto decision tree + reflection-driven auto-tracing. Citation: wro.cpp 2026-05-20.

## Suggested post time
Wednesday 2026-05-20, 10:00 CET
Reason: First MR5 launch slot in the performance cluster.
