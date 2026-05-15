# reflect_tracing: ~200 ns per span, function-address payload, Chrome / Perfetto JSON dump

## Body
Tracing and metrics split into sibling libraries: `reflect_telemetry` (post 23) for aggregates over time, `reflect_tracing` for spans at microsecond resolution. The hot-path engine is **Maciek Gajewski's 2021 wro.cpp technique**: thread-local ring buffers, ~200 ns per span, function address as payload, DWARF resolution at dump time. The reflection contribution is the instrumentation layer.

Today (C++26): one explicit scope-guard per traced function. Reflection at compile time gives you the function's name, signature, source location -- no `__PRETTY_FUNCTION__` macro, no preprocessor magic:

```cpp
void with_reflection() {
    auto _ = trace::span<^^&with_reflection>{};   // 200 ns
    // ... function body
}

// at shutdown, or on signal:
trace::dump_chrome_json("/tmp/trace.json");
```

Output (Chrome / Perfetto trace JSON -- both speak the same dialect):

```json
{"traceEvents":[
  {"name":"with_reflection",     "ph":"X","ts":230302784328,"dur":0,"pid":1,"tid":0},
  {"name":"void with_nttp_named()","ph":"X","ts":230302784329,"dur":0,"pid":1,"tid":0},
  ...
]}
```

Open in `chrome://tracing` or Perfetto's web UI; navigate the call graph at flame-graph zoom; correlate with metrics from reflect_telemetry on the same struct definitions. Hot path is one cache-line write per span; cold path is the dump (DWARF resolution amortised).

Tomorrow (C++29): `[[trace]]` annotation + P3294 token injection makes the scope-guard line invisible. The compiler inserts the trace at function entry; the tracing surface shrinks to "annotate the functions you want, leave the rest alone".

What this REPLACES: ad-hoc `clock::now()` + log-line trace patterns; per-team tracing macros (Tracy / EASY_PROFILER are great but each has its own integration story); the hand-written JSON-emit code that ships sideways through the build.

What this does NOT replace: distributed tracing (W3C Trace-Context headers across service boundaries -- still OpenTelemetry's job); span sampling strategies (your collector); cross-process correlation. The reflection layer is the in-process span surface; the rest is operational tracing infrastructure.

Series post 24 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996.

https://wrocpp.github.io/posts/reflect-tracing/

## Hashtags
#cpp #cpp26 #reflection #tracing #perfetto #chrome #observability #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_tracing". Subhead: ~200 ns per span; reflection-driven instrumentation; Chrome / Perfetto JSON dump. Citation: wro.cpp 2026-06-27.

## Suggested post time
Saturday 2026-06-27, 10:00 CET
Reason: Saturday morning EU C++ + perf-engineering audience; reflection-arc post 24 continues the every-2-day cadence.
