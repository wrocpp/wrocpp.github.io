# One Qt class template can declare typed signals without moc

## Body
moc cannot compile a class template with signals, so a Qt team had split every observable container in two and copied the wiring into 19 files.

reflect-moc now builds one container template with typed signals, and one model serves seven Qt containers. The cause was a single line: a template specialization has no identifier. A mirror of what a view would see is compared with the model after 224,000 random steps, and six deliberately wrong adapters are all caught.

GCC only, and QMultiMap is not supported. The post lists the limits.

https://wrocpp.github.io/posts/qt-class-template-typed-signals-without-moc/

## Hashtags
#cpp #cpp26 #qt #reflection #moc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "moc can't read a template. Reflection can." with a subtitle saying one container template with typed signals, one model for seven Qt containers and tests that catch six wrong adapters. Citation footer: wro.cpp, 2026-10-22.

## Suggested post time
Thursday 2026-10-22, 08:00 UTC
Reason: first post of the day; the Rust and Swift interop news holds the 16:00 UTC slot.
