# A stdexec task next to a generator (a reference implementation, not std::execution::task)

## Body
This post is about exec::task from NVIDIA's stdexec library. It is not the standard's std::execution::task, which cannot be tried yet: the feature-test macros are undefined on GCC 16.2 and trunk.

exec::task builds and runs on GCC 16.2 and Clang trunk. One task is 1 allocation of 168 to 176 bytes, and a task that awaits two tasks is 3. A generator for three values is 1 allocation, or none on Clang at -O2. A const& parameter dangles in a task just as in a generator, and AddressSanitizer reports stack-use-after-scope on both compilers.

GCC trunk stops with an internal compiler error on the task header. The library on Compiler Explorer has no version macro, so the date, 2 November 2026, is the pin.

https://wrocpp.github.io/posts/task-next-to-a-generator/

## Hashtags
#cpp #cpp26 #coroutines #stdexec #execution #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "This task is stdexec's, not the standard's" with a subtitle about allocation counts and a dangling const& parameter. Citation footer: wro.cpp, 2026-11-30.

## Suggested post time
Monday 2026-11-30, 08:00 UTC
Reason: the morning slot, the last of the generator and coroutine posts.
