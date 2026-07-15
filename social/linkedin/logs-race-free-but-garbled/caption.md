# Your std::cout logging has no data race and still tears

## Body
Qt's qInstallMessageHandler ships with one line of fine print: the handler must be reentrant, because Qt may call it from several threads at once. So your log callback runs concurrently, and every write to a shared sink races the others.

Point it at std::cout and it neither crashes nor corrupts anything. It just prints garbage. Three threads writing six lines each, and the records tear into one another: one thread opens a line, another cuts in before it finishes, and the prefixes and numbers splice together.

The C++ standard is precise about why. Concurrent use of a synchronized cout is guaranteed free of data races, so no undefined behavior, as long as sync_with_stdio stays true. But that is all it guarantees. Each << is a separate synchronized operation, and between two of them another thread's output can land. The standard removes the data race and leaves the race condition.

"Thread-safe" gets used for both properties, which is why this catches people out. cout is thread-safe for correctness and not thread-safe for readability. Closing that gap is what C++20, C++23, and C++26 have been doing.

Episode 1 of a new series on concurrent I/O in C++.

https://wrocpp.github.io/posts/logs-race-free-but-garbled/

## Hashtags
#cpp #cplusplus #cpp20 #concurrency #multithreading #logging #iostream #moderncpp

## Alt-text
A cream wro.cpp card reading "Race-free logs that still come out garbled", on concurrent std::cout output.

## Suggested post time
Friday 2026-09-04, 10:00 CET
Reason: morning CET; the series runs on Fridays.
