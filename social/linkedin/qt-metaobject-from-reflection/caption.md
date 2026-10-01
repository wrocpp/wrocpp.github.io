# Qt accepts a QMetaObject that C++26 reflection built

## Body
Qt 6.10 builds its meta-objects from constexpr tables. So a table made by C++26 reflection goes in the same place, and Qt does not notice.

The class in the post has no Q_OBJECT, no signals: or slots: section, and the build does not run moc. QMetaObject::method(i) still reports a signal, two slots and a plain method. Stock Qt connects to them, invokes them, reads the properties, casts with qobject_cast and binds them in QML. A differential test compares the result with the QMetaObject moc generates for the same class, and the two are identical.

Four things had to be worked around on GCC 16.2, and a signal's declaration had to change. The post lists all five. The output comes from a Docker run with GCC 16.2.0 and Qt 6.10.3, not from Compiler Explorer, and the post says so. It is also a correction to post 17, which called this a bigger project than a blog post. The first working version is one file of 516 lines.

https://wrocpp.github.io/posts/qt-metaobject-from-reflection/

If you maintain a Qt codebase, which part of moc would you miss first?

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "Qt runs a class that moc never saw" with a subtitle saying that C++26 reflection builds the QMetaObject, that stock Qt 6.10 connects, invokes and binds it in QML, and that a differential test finds it identical to moc's. Citation footer: wro.cpp, 2026-10-06.

## Suggested post time
Tuesday 2026-10-06, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
