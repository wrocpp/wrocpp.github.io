# Closing the known limits of the Qt observable models

## Body
The first post on observable Qt containers ended with a list of ten limits. This one closes most of them and says what is left.

Tests written for the limits found three defects. A list model answered the key role with the row, which shifts without a signal, so a sorting proxy went stale. A pointer to a class template specialization aborted Qt because GCC spells the name differently from Qt's normalizer. And a 1.7 times slowdown in hash removal on x86_64 turned out to be the same scan loop landing across a 32-byte boundary in one build.

A row index then made a change 50 to 200 times cheaper at 100,000 entries for a hash and 10,000 for a map, and QMultiMap and QMultiHash now work with an entry named by its key and occurrence. The speed numbers come from one Mac and one CI runner, nothing ran on clang, and I still have not seen the code that started this.

https://wrocpp.github.io/posts/qt-observable-models-known-limits/

## Hashtags
#cpp #cpp26 #qt #reflection #moc #performance #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A 1.7x slowdown that was only code placement" with a subtitle about closing the known limits of the Qt observable models. Citation footer: wro.cpp, 2026-10-28.

## Suggested post time
Wednesday 2026-10-28, 16:00 UTC
Reason: second post of the day; the planned-double slot in scripts/schedule_doubles.py.
