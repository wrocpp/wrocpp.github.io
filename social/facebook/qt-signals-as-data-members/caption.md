# C++26 cannot write a signal's body, so a signal became a data member

## Body
A Qt signal is a function whose body moc writes, and C++26 reflection can only add data members to a class, not function bodies. So in reflect-moc a signal is a data member.

The post shows three designs that failed, the one that held (8 bytes per signal, 8 per class) and a static form that costs 0 bytes per signal and has one silent pitfall: emit other->s(v) fires on this.

It is GCC 16.2 only, measured with Qt 6.10.3 on aarch64 in Docker, and the library is not published yet. The previous episode is at https://wrocpp.github.io/posts/qt-metaobject-from-reflection/

https://wrocpp.github.io/posts/qt-signals-as-data-members/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "C++26 cannot write a signal's body" with a subtitle about a signal as a data member costing 8 bytes, and a static signal costing 0 bytes with one silent pitfall. Citation footer: wro.cpp, 2026-10-09.

## Suggested post time
Friday 2026-10-09, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
