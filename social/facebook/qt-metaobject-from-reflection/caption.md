# Qt accepts a QMetaObject that C++26 reflection built

## Body
Qt 6.10 builds its meta-objects from constexpr tables, so a table made by C++26 reflection goes in the same place.

A class with no Q_OBJECT and no moc step now connects, invokes, exposes properties and binds in QML on stock Qt. A differential test finds its QMetaObject identical to the one moc generates. The post also lists the four things that had to be worked around on GCC 16.2.

https://wrocpp.github.io/posts/qt-metaobject-from-reflection/

Would you drop moc from your build if you could?

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "Qt runs a class that moc never saw" with a subtitle about C++26 reflection building a QMetaObject that stock Qt 6.10 accepts. Citation footer: wro.cpp, 2026-10-06.

## Suggested post time
Tuesday 2026-10-06, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
