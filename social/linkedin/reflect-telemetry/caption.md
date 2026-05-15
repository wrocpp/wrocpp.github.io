# reflect_telemetry: annotate fields, get a Prometheus + OpenTelemetry exporter

## Body
Every microservice has hand-registered `counter.WithLabel("http_requests_total").Inc()` lines that drift from the variable they actually count. C++26 reflection collapses the registration: annotate a field with `[[=metric(counter)]]` or `[[=metric(gauge)]]`; reflection emits the Prometheus exposition + OpenTelemetry OTLP exporter from the struct shape:

```cpp
struct Metrics {
    [[=metric{kind::counter, "Total HTTP requests."}]]
    std::atomic<uint64_t> http_requests_total = 42;

    [[=metric{kind::gauge, "Open connections."}]]
    std::atomic<uint64_t> http_open_connections = 7;
};

std::println("{}", reflect_telemetry::expose<Metrics>(m));
```

Output (Prometheus exposition format -- the standard `/metrics` endpoint shape):

```
# TYPE http_requests_total counter
http_requests_total 42
# HELP http_open_connections Open connections.
# TYPE http_open_connections gauge
http_open_connections 7
```

The mechanic: walk `nonstatic_data_members_of(^^Metrics)`; per member, read the P3394 `metric` annotation for kind + help text; emit `# TYPE` / `# HELP` / value. Add a metric, the exposition updates. Rename a metric, the wire format renames. Remove a metric, it vanishes from `/metrics` next build.

What this REPLACES: the parallel `prometheus.cpp` registration file every service maintains, the test that verifies you remembered to register the new counter, the late-night incident where a critical metric was added to the struct but not to `/metrics`.

What this does NOT replace: histogram bucket strategy (still your call), label cardinality discipline (the kind of mistake that takes Prometheus down), the metric-to-alert mapping in your monitoring stack. The reflection layer is the schema-to-exposition pipe; everything else is operational.

The pattern is genuinely novel -- nobody is doing this in C++ today. Rust has `metrics-derive` for the runtime-attribute-based version; the C++26 compile-time-attribute version is a wro.cpp first.

Series post 23 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996.

https://wrocpp.github.io/posts/reflect-telemetry/

## Hashtags
#cpp #cpp26 #reflection #observability #prometheus #opentelemetry #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_telemetry". Subhead: P3394 [[=metric(...)]] annotations + reflection emit Prometheus / OpenTelemetry exposition from struct shape. Citation: wro.cpp 2026-06-25.

## Suggested post time
Thursday 2026-06-25, 10:00 CET
Reason: Mid-week morning EU C++ + observability audience; reflection-arc post 23 continues the every-2-day cadence.
