# Signals and slots across threads without Qt

## Body
The core of reflect-moc, signals, slots, queued and blocking connections and thread affinity, works in plain C++26 with no Qt and no moc. A worker thread reports progress to an object on the main thread, and neither class owns a mutex or a queue.

Under ThreadSanitizer one test reports in 27 of 11000 repeats. A 12-line std::latch program with no library code reports in 132 of 11000, and a mutex with a condition variable gives 0 of 11000. I read it as a ThreadSanitizer limitation with std::latch, not a race in the library, from the header only.

GCC 16.2 only, ThreadSanitizer on aarch64 in Docker. The library is published at https://github.com/wrocpp/reflect-moc (experimental; GCC 16.2, Qt 6.10.3, aarch64 Docker only).

https://wrocpp.github.io/posts/signals-slots-threads-without-qt/

Earlier episodes: https://wrocpp.github.io/posts/qt-metaobject-from-reflection/, https://wrocpp.github.io/posts/qt-signals-as-data-members/ and https://wrocpp.github.io/posts/qt-object-that-never-names-its-class/

## Hashtags
#cpp #cpp26 #reflection #qt #threadsanitizer #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "Signals and slots across threads without Qt" with a subtitle naming direct, queued and blocking delivery, thread affinity and a ThreadSanitizer result with its caveat. Citation footer: wro.cpp, 2026-10-15.

## Suggested post time
Thursday 2026-10-15, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
