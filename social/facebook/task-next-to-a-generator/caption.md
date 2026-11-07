# A stdexec task next to a generator (a reference implementation, not std::execution::task)

## Body
The task in this post is exec::task from NVIDIA's stdexec, not the standard's std::execution::task. On GCC 16.2 and Clang trunk one task is a single allocation of 168 to 176 bytes. A const& parameter dangles in a task as it does in a generator.

https://wrocpp.github.io/posts/task-next-to-a-generator/

## Hashtags
#cpp #cpp26 #coroutines #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "This task is stdexec's, not the standard's" with a subtitle about allocation counts and a dangling const& parameter. Citation footer: wro.cpp, 2026-11-30.

## Suggested post time
Monday 2026-11-30, 08:00 UTC
Reason: the morning slot, the last of the generator and coroutine posts.
