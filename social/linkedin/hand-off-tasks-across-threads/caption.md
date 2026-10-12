# Hand a task to another thread without leaving a copy behind

## Body
Last week's short showed that libc++ leaves a copy of a small callable in a moved-from std::function. This one tests two fixes for a task that crosses several layers into a queue on another thread.

The demo sends one task through two layers three ways. A chain of by-value parameters still destroys the captured resource on the sending thread on libc++. Taking the task by rvalue reference and emptying it with std::exchange destroys it on the worker. So does boxing it in a shared_ptr at the entry point.

My first version had both fixes and still failed, because the harness passed the task by value into the first layer. The thread printed at the end caught it.

https://wrocpp.github.io/posts/hand-off-tasks-across-threads/

## Hashtags
#cpp #cplusplus #libcxx #concurrency #qt #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Two ways to stop std::move leaving a copy behind" with a subtitle saying that on libc++ an exchange or a shared_ptr box destroys the task on the worker thread. Citation footer: wro.cpp, 2026-10-19.

## Suggested post time
Monday 2026-10-19, 16:00 UTC
Reason: second post of the day; the Qt examples post holds the 08:00 UTC slot.
