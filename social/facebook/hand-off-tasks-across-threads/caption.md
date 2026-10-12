# Hand a task to another thread without leaving a copy behind

## Body
Two fixes for a std::function that keeps a copy of its callable after a move on libc++: empty it with std::exchange, or box it in a shared_ptr at the entry point. A demo shows both destroy the task on the worker thread, while a plain by-value chain does not.

https://wrocpp.github.io/posts/hand-off-tasks-across-threads/

## Hashtags
#cpp #cplusplus #libcxx #concurrency #qt #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Two ways to stop std::move leaving a copy behind" with a subtitle saying that on libc++ an exchange or a shared_ptr box destroys the task on the worker thread. Citation footer: wro.cpp, 2026-10-19.

## Suggested post time
Monday 2026-10-19, 16:00 UTC
Reason: second post of the day; the Qt examples post holds the 08:00 UTC slot.
