# Structured concurrency: what std::future never had

## Body
A std::future is a dead end: you launch it, you get() it once, and composing two of them means manual threads and locks. C++26 senders compose -- and the composition stays structured.

With std::execution you express "run these two things concurrently, then continue once both finish" as a single value. when_all(a, b) is itself a sender: it starts both, completes when both finish, and carries both results. Run them on a static_thread_pool scheduler and you write no mutex and no join -- the pool's destructor cleans up, and there is no detached thread to outlive main.

That is the structural win. when_all(a, b) is a value, so you can hand it to another adaptor and keep building: schedule it, chain a step that runs once both complete, race it against a timeout. A future is a leaf you consume once; a sender is a node you grow a graph from. Swap the thread pool for a GPU stream scheduler and the same graph runs on the device.

Runnable on Compiler Explorer (GCC 16.1 + clang-p2996), using NVIDIA's stdexec reference implementation:

https://wrocpp.github.io/posts/structured-concurrency/

## Hashtags
#cpp #cpp26 #stdexecution #concurrency #parallelism #cpplang #wrocpp

## Alt-text
A dark wro.cpp social card with the line "A std::future is a dead end. A C++26 sender is a node you keep building a graph from."

## Suggested post time
Tuesday 2026-06-30, 10:00 CET
Reason: matches the publish date; Tuesday mid-morning is a strong weekday slot for technical reach.
