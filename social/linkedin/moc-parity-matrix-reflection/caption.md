# Replacing moc with reflection: 35 of 48 matrix rows match, and a class needs no macro

## Body
I wrote down 48 things moc processes or generates, one row each, and tested every verdict. A "same" row builds the class for real moc next to the reflect-moc version and compares the two meta-objects row for row, then runs both. 35 rows are the same (30 checked against a real moc, 5 by behaviour moc cannot give), 7 differ in a way the note names, and 4 are not supported yet.

A Qt class, a derived class, a widget class and a gadget now need no macro and no moc input. The base class finds the class it belongs to through a default template argument, so the class is never named twice.

Each open row has a reason: private slots and properties, the input of qmltyperegistrar, and namespaces and plugin metadata, which work with a stated catch. The observable container from the spec series is one use case among them.

https://wrocpp.github.io/posts/moc-parity-matrix-reflection/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A Qt class with no macro and no moc" with a subtitle about 35 of 48 rows of a moc conformance matrix being the same, 30 checked against a real moc. Citation footer: wro.cpp, 2026-10-29.

## Suggested post time
Thursday 2026-10-29, 16:00 UTC
Reason: the second slot of the day, the flagship of the Qt series, a few days after the spec post.
