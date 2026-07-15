# The fastest loggers do not format on the calling thread

## Body
osyncstream, mutex, and std::print all synchronize on the calling thread. Fine for most code, a problem on a latency-critical path.

The fast answer: callers push a raw record to a queue and return; a background thread formats and writes it. The demo is a mini version. Real loggers sharpen it: spdlog around 250 ns per call, Quill and NanoLog nearer 7 to 11 ns by deferring formatting off the thread.

The trade-off: queued records can be lost in a crash, and a full queue means blocking or dropping.

Episode 9, the last, of the concurrent I/O series.

https://wrocpp.github.io/posts/loggers-off-thread/

## Hashtags
#cpp #cplusplus #concurrency #logging #performance
