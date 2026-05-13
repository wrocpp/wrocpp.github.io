# Profiling C++ in 2026 -- perf / Tracy / Perfetto, plus reflection-driven auto-tracing

## Body
"What profiler should I use?" is the wrong question in C++ in 2026. You'll reach for three or four -- not because the field is fragmented, but because sampling, instrumentation, PMU counters, and cache-level attribution each answer different questions:

- **perf** -- system-wide sampling, ~1% overhead, zero code change. First-pass diagnosis: "where is my time going?"
- **Tracy** -- frame-aware zones, ~1 ns/zone. Tick loops, render threads, game engines.
- **Perfetto** -- multi-process trace with kernel events. Distributed systems, cross-thread correlation.
- **Callgrind** -- exact call counts at 50x slowdown. Cycle-accurate diagnosis runs.
- **VTune** -- proprietary Intel x86, cache-misses + branch-mispredict + memory traffic.

The new wro.cpp Toolset launch (MR5 in the performance cluster) covers the decision tree end-to-end -- when each tool wins, the CI recipes, and the instrumentation tax each costs. But the more interesting part is the C++26 reflection pattern that eliminates the per-method tracing boilerplate every team carries.

Production tracing today: every codebase has a `TRACE_EVENT_BEGIN("draw"); ... TRACE_EVENT_END();` macro at every zone boundary. The wrapping is mechanical, and humans forget to add it exactly where the next bottleneck lives -- the method shipped last sprint that's now eating 40% of latency. P3394 annotations turn opt-in into a one-line marker:

```cpp
struct Renderer {
    [[=trace{}]] std::function<void(std::string_view)> draw;
    [[=trace{}]] std::function<void(int)>              flush;
                 std::function<void()>                 invisible;  // no trace
};

auto r = instrument(Renderer{...});   // reflection walks members, wraps annotated ones
r.draw("frame 1");                    // -> span_log records (name="draw", duration=292ns)
```

The reflection harness is identical across Tracy / Perfetto / OpenTelemetry / chrome-trace -- only the sink changes. `span_log().push_back(...)` becomes `ZoneScopedN(name)` (Tracy) or `TRACE_EVENT_INSTANT(name)` (Perfetto). Add a method, the trace point follows automatically when re-annotated; remove the annotation, the wrapper evaporates.

What it does NOT replace: sampling profilers (still needed for third-party / kernel attribution), async-trace correlation (context propagation stays separate), PMU counters (hardware features that user code can't synthesise).

C++29 token injection (P3294) takes the pattern further: the annotation on the interface triggers the compiler to inject the wrapper as generated code -- no std::function indirection, zero per-call overhead.

https://wrocpp.github.io/toolset/profiling-cpp-2026/

## Hashtags
#cpp #cpp26 #profiling #performance #perf #tracy #perfetto #reflection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Profiling C++ in 2026". Subhead: perf / Tracy / Perfetto / Callgrind / VTune decision tree, plus reflection-driven auto-tracing via P3394 annotations. Citation: wro.cpp 2026-05-20.

## Suggested post time
Wednesday 2026-05-20, 10:00 CET
Reason: Mid-week morning slot reaches EU C++ engineers in flow. MR5 toolset launch -- first entry in the new performance cluster.
