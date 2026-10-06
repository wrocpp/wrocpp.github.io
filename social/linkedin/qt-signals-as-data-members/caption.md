# C++26 cannot write a signal's body, so a signal became a data member

## Body
A Qt signal is a function that moc defines for you. C++26 reflection can list a class's signals, but define_aggregate only adds data members, so it cannot write a function body.

The post, the second in the reflect-moc series, covers three designs that did not work. A callable data member does not connect, because Qt reads the class of a signal from QtPrivate::FunctionPointer, which exists only for pointers to member functions. A std::source_location tag gives every member the same type. A closure tag gives each member its own type, but that type has internal linkage and GCC warns about it with -Wsubobject-linkage.

What held is a data member with no body that finds its owner through a hidden first member. It costs 8 bytes per signal and 8 per class, and stock connect, QSignalSpy and QML accept it. A static form costs 0 bytes per signal and also connects, with one silent pitfall: emit other->s(v) on another instance of the same class fires on this. A one-line function body that calls rqt::activate is the one form that handles overloaded signals.

The limits are in the post. Everything is GCC 16.2 only, with Qt 6.10.3 on aarch64 in Docker. Compiler Explorer has no Qt it can link, so the Qt-free demo runs there and the connect errors are quoted. The emit timings came from a loaded Mac and show no difference. The library is published at https://github.com/wrocpp/reflect-moc (experimental; GCC 16.2, Qt 6.10.3, aarch64 Docker only).

https://wrocpp.github.io/posts/qt-signals-as-data-members/

The previous episode shows stock Qt accepting a QMetaObject built by reflection: https://wrocpp.github.io/posts/qt-metaobject-from-reflection/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "C++26 cannot write a signal's body" with a subtitle saying that a signal became a data member costing 8 bytes each, and that a static signal costs 0 bytes and has one silent pitfall. Citation footer: wro.cpp, 2026-10-09.

## Suggested post time
Friday 2026-10-09, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
