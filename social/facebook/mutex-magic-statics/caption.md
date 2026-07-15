# static std::mutex is safe to construct, thanks to magic statics

## Body
The pre-osyncstream fix for a shared log sink: a static std::mutex plus a lock_guard around every write.

But is the static mutex itself safe to initialize when two threads reach it at once? Yes. Since C++11, a function-local static is constructed exactly once, even under contention; the second thread waits for the first. The demo counts constructor calls under a three-thread stampede and gets one.

It was undefined before C++11, and MSVC only shipped it in VS 2015. Today it costs a single guard-flag check.

Episode 3 of a series on concurrent I/O.

https://wrocpp.github.io/posts/mutex-magic-statics/

## Hashtags
#cpp #cplusplus #cpp11 #concurrency #programming
