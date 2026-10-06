# Replaying Qt Bridges' meta-object calls in C++ and diffing them against moc

## Body
A property declared with a getter and nothing else is read-only in moc. Built the way Qt Bridges' Rust layer builds it, the same property reports as writable, and a QML assignment to it is accepted without an error.

I replayed the layer's QMetaObjectBuilder calls in C++ for one small class and compared the meta-object with moc's, on Qt 6.10.3, 6.11.3 and 6.12.0. The Rust layer's registration API has no way to mark a property read-only, to name a signal's parameters or to add an enum, so an implicit onMoved handler that uses from and to fails with a ReferenceError. The dumps are identical across the three Qt versions.

In a C++ analogue of the Rust emit path, emitting a signal by name costs about 22 to 46 ns more than emitting it by index. The machine was busy, so read that as a rough size.

Qt Bridges targets other languages and is in beta, and reflect-moc is a C++ analogue, so this compares two ways to produce a QMetaObject on one class and not the products. No Rust was built or run. The post gives the source commits and line numbers, and lists what was not tested.

https://wrocpp.github.io/posts/replay-qt-bridges-meta-objects-against-moc/

## Hashtags
#cpp #qt #moc #qml #rust #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "A read-only Qt property that QML can write" with a subtitle saying that in a C++ replay of Qt Bridges' Rust builder calls a getter-only property accepts a QML assignment while moc throws a TypeError. Citation footer: wro.cpp, 2026-10-21.

## Suggested post time
Wednesday 2026-10-21, 16:00 UTC (18:00 CEST)
Reason: the planned second post of the day (scripts/schedule_doubles.py), beside the evergreen post of the 08:00 UTC slot.
