# static std::mutex is safe to construct, thanks to magic statics

## Body
Before C++20's osyncstream, the fix for a shared log sink was a mutex: guard every write with a static std::mutex and a lock_guard, and the threads take turns.

The static local raises a question, though. It is initialized the first time control reaches the declaration, so what if two threads reach it at once? Do they both construct the mutex, or use it half-built?

Neither. Since C++11, function-local statics have a thread-safe initialization guarantee, the feature people call "magic statics": if one thread is initializing the variable, any other thread that arrives waits until it finishes. Exactly one construction. The demo proves it by counting constructor calls under a three-thread stampede: the count is one.

This was undefined before C++11 (hence double-checked locking, easy to get wrong). GCC and Clang had it early; MSVC only shipped it in Visual Studio 2015. The steady-state cost is a single relaxed guard-flag load, so the lazy static singleton is finally both correct and cheap.

Mutex or osyncstream? The mutex serializes the whole write; osyncstream formats in parallel and serializes only the emit. The mutex has one edge: it does not need the whole program to cooperate.

Episode 3 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/mutex-magic-statics/

## Hashtags
#cpp #cplusplus #cpp11 #concurrency #multithreading #mutex #moderncpp

## Alt-text
A cream wro.cpp card reading "static std::mutex initializes itself, safely", on C++11 magic statics.

## Suggested post time
Friday 2026-09-18, 10:00 CET
Reason: morning CET; Friday series lane.
