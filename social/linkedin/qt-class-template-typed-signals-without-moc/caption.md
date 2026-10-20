# One Qt class template can declare typed signals without moc

## Body
Leonardo Rossi wrote that reflect-moc still lists one limit that is exactly his case: a class template with signals. His team split every observable container into a signals base keyed by QVariant and a typed template, and copied the wiring into 19 files.

The cause was one line. A template specialization has no identifier, and the code that names a class asked for one. With that fixed, one ObservableContainer<C> declares typed signals, and one ContainerModel<C> serves QList, QMap, QHash and four more containers.

To look for ghost rows, a mirror built from the model's signals alone is compared with the live model after 224,000 random steps. Six deliberately wrong adapters are all reported, and 30 of 31 mutants are killed. I have not seen his code, QMultiMap is not supported, and the library is GCC only.

https://wrocpp.github.io/posts/qt-class-template-typed-signals-without-moc/

## Hashtags
#cpp #cpp26 #qt #reflection #moc #softwarearchitecture #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "moc can't read a template. Reflection can." with a subtitle saying one container template with typed signals, one model for seven Qt containers and tests that catch six wrong adapters. Citation footer: wro.cpp, 2026-10-22.

## Suggested post time
Thursday 2026-10-22, 08:00 UTC
Reason: first post of the day; the Rust and Swift interop news holds the 16:00 UTC slot.
