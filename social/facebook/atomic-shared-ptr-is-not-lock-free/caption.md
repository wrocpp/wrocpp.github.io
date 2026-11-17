# std::atomic<std::shared_ptr> is not lock-free in libstdc++ or the MSVC STL

## Body
Atomic shared_ptr removes the data race of a plain shared_ptr, and is_lock_free() is still false on GCC 16.2, GCC trunk and MSVC. libstdc++ and the MSVC STL keep a lock bit in the control-block pointer. On GCC 16.2 a load has 3 locked instructions and a plain copy has 1. Clang with libc++ does not compile the type.

https://wrocpp.github.io/posts/atomic-shared-ptr-is-not-lock-free/

## Hashtags
#cpp #cpp20 #atomic #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Atomic shared_ptr is not lock-free" with a subtitle: is_lock_free() is false on GCC 16.2, GCC trunk and MSVC, a load takes 3 locked instructions against 1 for a plain copy, and libc++ does not compile it. Citation footer: wro.cpp, 2026-12-22.

## Suggested post time
Tuesday 2026-12-22, 08:00 UTC
Reason: the morning slot on the publication day.
