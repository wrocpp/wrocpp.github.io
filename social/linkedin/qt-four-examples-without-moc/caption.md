# Four official Qt examples build and run without moc

## Body
I took four examples from Qt 6.10.3 (a QThread renderer, a QML tutorial, a widgets example and a queued custom type) and let a migration tool rewrite them for reflect-moc. Then I built each one with AUTOMOC off.

Each example prints the same harness output as the moc build, with 0 warnings. A build in which moc is replaced by a failing trap passes, so no moc ran. The diffs are 14 to 111 changed lines, and the tool left nothing for manual work.

The post also lists what these checks do not show: the examples are four, the numbers come from the repository's own harness, and the build times carry timing noise.

The library is public at https://github.com/wrocpp/reflect-moc

https://wrocpp.github.io/posts/qt-four-examples-without-moc/

Earlier episodes: https://wrocpp.github.io/posts/qt-metaobject-from-reflection/, https://wrocpp.github.io/posts/qt-signals-as-data-members/ and https://wrocpp.github.io/posts/qt-object-that-never-names-its-class/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "Four official Qt examples, built with moc off" with a subtitle saying that a failing trap stands in for moc and each example still prints the same output as the original build. Citation footer: wro.cpp, 2026-10-19.

## Suggested post time
Monday 2026-10-19, 08:00 UTC (10:00 CEST)
Reason: the flagship slot of the day, a single post.
