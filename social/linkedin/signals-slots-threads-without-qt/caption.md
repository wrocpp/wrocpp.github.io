# Signals and slots across threads without Qt

## Body
The fourth episode of the reflect-moc series leaves Qt out. The core of the library is signals, slots, queued and blocking connections, thread affinity and a per-thread event loop in plain C++26, with no Qt and no moc.

The example is a worker on a background thread reporting progress to an object on the main thread. Neither class owns a mutex or a queue. Each connection compares the receiver's thread with the emitting one: a slot runs directly on the same thread and is queued to the receiver's thread otherwise, with its arguments copied. A blocking connection makes the emitter wait until the slot has run. Both programs run on Compiler Explorer.

Connections are not stored by signal index. Each sender holds a mutex-guarded vector of records, and an emit copies the matching ones, so a slot may disconnect itself while it runs.

Under ThreadSanitizer the 18 core tests passed in the recorded run. One test, which waits on a std::latch, reported two data races in 27 of 11000 repeats. A 12-line program with only a std::latch reports in 132 of 11000, and a mutex with a condition variable, or a binary semaphore, gives 0 of 11000. I read that as a ThreadSanitizer limitation with std::latch in libstdc++, not a race in the library. That reading comes from the header. I did not read the library's wait function or run the experiment that would confirm it.

The limits are in the post. GCC 16.2 only, ThreadSanitizer on aarch64 in Docker only. The library is published at https://github.com/wrocpp/reflect-moc (experimental; GCC 16.2, Qt 6.10.3, aarch64 Docker only).

https://wrocpp.github.io/posts/signals-slots-threads-without-qt/

Earlier episodes: https://wrocpp.github.io/posts/qt-metaobject-from-reflection/, https://wrocpp.github.io/posts/qt-signals-as-data-members/ and https://wrocpp.github.io/posts/qt-object-that-never-names-its-class/

## Hashtags
#cpp #cpp26 #reflection #qt #threadsanitizer #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "Signals and slots across threads without Qt" with a subtitle naming direct, queued and blocking delivery, thread affinity and a ThreadSanitizer result with its caveat. Citation footer: wro.cpp, 2026-10-15.

## Suggested post time
Thursday 2026-10-15, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
