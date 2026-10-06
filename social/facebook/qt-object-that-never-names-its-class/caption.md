# A Q_OBJECT that never names its class

## Body
Q_OBJECT does not say which class it sits in, and neither does RQT_OBJECT in reflect-moc. It finds the class by asking std::meta::current_function() for its parent from inside member functions defined in the class body.

RQT_PROPERTY takes the exact Q_PROPERTY text and parses it in a consteval function, so a misspelled keyword stops the build with a named error.

The demo is a reduction without Qt, run on Compiler Explorer with GCC 16.2. The real macros were not rebuilt for this post, and the library is not published yet.

https://wrocpp.github.io/posts/qt-object-that-never-names-its-class/

Earlier episodes: https://wrocpp.github.io/posts/qt-metaobject-from-reflection/ and https://wrocpp.github.io/posts/qt-signals-as-data-members/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "A Q_OBJECT that never names its class" with a subtitle saying that Q_PROPERTY text is parsed by consteval code and that a typo stops the build with a named error. Citation footer: wro.cpp, 2026-10-12.

## Suggested post time
Monday 2026-10-12, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
