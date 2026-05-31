# Replacing Qt's MOC with reflection

## Body
Q_OBJECT and the moc compiler exist because C++ could not see inside your class. Properties, signals, and slots needed a preprocessor pass to generate the meta-object boilerplate.

C++26 reflection sees inside the class. nonstatic_data_members_of, annotations, and define_aggregate together give you properties, signal/slot wiring, and dynamic property access without a separate code generation step.

100 lines of header replace moc for the common case. Qt itself is exploring this (their QRangeModel hackathon). Full replacement still needs P3294 token injection (C++29 territory), but the property layer ships in C++26.

https://wrocpp.github.io/posts/qt-moc-replacement/

## Hashtags
#cpp #cpp26 #qt #moc #reflection #p2996 #signals #properties #wrocpp

## Alt-text
Editorial card: "Replacing Qt MOC with reflection". 100 lines of header replace the meta-object preprocessor.

## Suggested post time
Thursday 2026-06-11, 10:00 CET
