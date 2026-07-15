# Thread-safe is not reentrant, and the difference bites

## Body
Qt's message-handler docs ask for a reentrant handler, not just a thread-safe one, and a std::mutex gives you the second without the first.

A mutex-guarded counter across four threads is thread-safe. But a function that locks and then calls itself deadlocks on a plain std::mutex; it needs a std::recursive_mutex. Thread-safe, not reentrant.

The rule: reentrant implies thread-safe and async-signal-safe, never the reverse. A signal handler re-entering a locked function deadlocks against itself.

Episode 8 of a series on concurrent I/O.

https://wrocpp.github.io/posts/reentrant-vs-thread-safe/

## Hashtags
#cpp #cplusplus #concurrency #programming #multithreading
