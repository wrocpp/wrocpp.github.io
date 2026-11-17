# std::atomic<std::shared_ptr> is not lock-free in libstdc++ or the MSVC STL

## Body
Yahav Gabay's LinkedIn post on atomic shared_ptr for config hot reload made me read what load() does.

A plain shared_ptr shared between threads is a data race. ThreadSanitizer on GCC 16.2 reports it in the copy constructor, exit code 66. The atomic version is clean under the same sanitizer.

It is also not lock-free. is_lock_free() and is_always_lock_free are false on GCC 16.2, GCC trunk, Clang 22.1 with libstdc++ and MSVC, and sizeof is 16, the same as a plain shared_ptr. I read libstdc++ 16 and the MSVC STL: both keep a lock in the low bits of the control-block pointer. libstdc++ spins on it, the MSVC STL waits on it.

A load has 3 locked instructions on GCC 16.2, a plain copy has 1. In one thread the fastest runs took 26.9 ns against 19.3 ns. I do not publish readers against a writer, because Compiler Explorer gave 2 cores and the runs varied too much. Clang with libc++ does not compile the type, and <hazard_pointer> and <rcu> were missing on every compiler I tried.

https://wrocpp.github.io/posts/atomic-shared-ptr-is-not-lock-free/

## Hashtags
#cpp #cpp20 #cpp26 #atomic #sharedptr #concurrency #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Atomic shared_ptr is not lock-free" with a subtitle: is_lock_free() is false on GCC 16.2, GCC trunk and MSVC, a load takes 3 locked instructions against 1 for a plain copy, and libc++ does not compile it. Citation footer: wro.cpp, 2026-12-22.

## Suggested post time
Tuesday 2026-12-22, 08:00 UTC
Reason: the morning slot on the publication day.
