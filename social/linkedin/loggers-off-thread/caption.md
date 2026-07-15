# The fastest loggers do not format on the calling thread

## Body
Everything in this series so far synchronizes on the calling thread. osyncstream buffers and emits there; the mutex serializes there; std::print locks the stream there. For most programs that is fine. On a latency-critical path, the formatting and I/O sitting on the caller's thread is the whole problem.

The production answer is to move both off the hot path. The caller hands a raw record to a queue and returns; a background thread pops records, formats, and writes. The demo is a mini version: application threads push a record, one worker thread does the formatting and output. Every line comes out whole for free, because only one thread ever touches the stream, and callers never pay for formatting or I/O.

Real low-latency loggers sharpen this. spdlog's async mode uses a pool behind a queue but still formats on the caller. Quill uses per-thread lock-free queues and defers formatting to the backend. NanoLog extracts static format text at compile time and logs only the dynamic values. The hot-path costs: spdlog around 250 ns per call, Quill and NanoLog in the 7-to-11 ns range.

The trade: queued records are not written yet, so a crash can lose them; ordering becomes the backend's job; a full queue means blocking or dropping. Correct output is a standard-library problem; fast enough is an architecture problem.

Episode 9, the last, of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/loggers-off-thread/

## Hashtags
#cpp #cplusplus #concurrency #logging #performance #hft #moderncpp

## Alt-text
A cream wro.cpp card reading "Your logger's real cost is on the hot path", on off-thread logging.

## Suggested post time
Friday 2026-10-30, 10:00 CET
Reason: morning CET; closes the series.
