# Replaying Qt Bridges' meta-object calls in C++ and diffing them against moc

## Body
A Qt property with only a getter is read-only in moc. Built the way Qt Bridges' Rust layer builds it, the same property reports as writable, and a QML assignment is accepted without an error.

I replayed the layer's builder calls in C++ for one class and compared the result with moc's on Qt 6.10.3, 6.11.3 and 6.12.0. No Rust was built or run, and the post lists what was not tested.

https://wrocpp.github.io/posts/replay-qt-bridges-meta-objects-against-moc/

## Hashtags
#cpp #qt #moc #qml #rust #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "A read-only Qt property that QML can write" with a subtitle saying that in a C++ replay of Qt Bridges' Rust builder calls a getter-only property accepts a QML assignment while moc throws a TypeError. Citation footer: wro.cpp, 2026-10-21.

## Suggested post time
Wednesday 2026-10-21, 16:00 UTC (18:00 CEST)
Reason: the planned second post of the day (scripts/schedule_doubles.py), beside the evergreen post of the 08:00 UTC slot.
