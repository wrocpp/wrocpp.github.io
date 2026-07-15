# Thread-safe is not reentrant, and the difference bites

## Body
The Qt documentation that started this series did not ask for a thread-safe handler. It asked for a reentrant one. Those are different requirements, and a std::mutex satisfies one without the other.

The demo has two halves. A shared counter guarded by a std::mutex, hammered by four threads, comes out exactly right: that is thread-safety. Then a function that locks and calls itself works only because the lock is a std::recursive_mutex; swap in a plain std::mutex and the second lock on the same thread would deadlock. Thread-safe, and not reentrant.

The taxonomy, precisely. Reentrant: can be entered again before a prior call finishes, even on the same thread, relying on no shared state and no non-recursive lock across the re-entry. Thread-safe: callable concurrently from many threads, often by taking a lock, which is what makes it non-reentrant. Async-signal-safe: callable from a signal handler. The implication runs one way. Reentrant implies the other two; thread-safe implies neither.

When Qt says reentrant, it is warning it may re-enter your handler from a nested call or a signal, not only another thread. C solved the same problem with flockfile's recursive per-FILE lock, the same shape as the recursive_mutex here.

Episode 8 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/reentrant-vs-thread-safe/

## Hashtags
#cpp #cplusplus #concurrency #reentrancy #multithreading #signals #moderncpp

## Alt-text
A cream wro.cpp card reading "Thread-safe code can still deadlock itself", on reentrancy versus thread-safety.

## Suggested post time
Friday 2026-10-23, 10:00 CET
Reason: morning CET; Friday series lane.
