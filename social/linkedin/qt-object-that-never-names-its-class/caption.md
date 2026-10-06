# A Q_OBJECT that never names its class

## Body
In Qt you write Q_OBJECT and never say which class it is in. The third episode of the reflect-moc series shows how a macro built on C++26 reflection does the same.

RQT_OBJECT expands to member functions defined in the class body. Inside one, std::meta::current_function() is that function and its parent is the class, so the macro needs no class name, no template base and no call in the constructor. A function body is a complete-class context, so reflection there also sees properties declared below the macro.

RQT_PROPERTY takes the exact Q_PROPERTY text, turns it into a string and parses it in a consteval function. The existing property lines keep working, and a keyword the parser does not know stops the build with a named error. In the library's differential test the eight Q_PROPERTY lines are identical for moc and for reflect-moc (I diffed them; I did not re-run that test).

The limits are in the post. The demo is a reduction without Qt, run on Compiler Explorer with GCC 16.2. The real RQT_OBJECT and RQT_PROPERTY were not rebuilt for this post, and current_function is not in clang-p2996. The library is published at https://github.com/wrocpp/reflect-moc (experimental; GCC 16.2, Qt 6.10.3, aarch64 Docker only).

https://wrocpp.github.io/posts/qt-object-that-never-names-its-class/

Earlier episodes: https://wrocpp.github.io/posts/qt-metaobject-from-reflection/ and https://wrocpp.github.io/posts/qt-signals-as-data-members/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "A Q_OBJECT that never names its class" with a subtitle saying that Q_PROPERTY text is parsed by consteval code and that a typo stops the build with a named error. Citation footer: wro.cpp, 2026-10-12.

## Suggested post time
Monday 2026-10-12, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
