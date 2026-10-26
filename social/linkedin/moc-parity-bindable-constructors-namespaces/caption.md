# Three more moc constructs without moc: BINDABLE, invokable constructors and namespaces

## Body
Three rows of the reflect-moc conformance matrix moved after the matrix post. BINDABLE properties and invokable constructors now equal moc's output row for row, and namespaces do so with three extra lines and an ordering rule, so that row stays partial.

Each has a parity test that builds the construct once with real moc and once with reflect-moc, and compares the meta-objects and the behaviour: bindings that follow a source, newInstance with default arguments, a JavaScript new, QMetaEnum::fromType on a namespace enum. Each test failed against a twin broken on purpose.

Five rows are still unsupported, and the post says why.

https://wrocpp.github.io/posts/moc-parity-bindable-constructors-namespaces/

## Hashtags
#cpp #cpp26 #qt #moc #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "BINDABLE, constructors, namespaces: no moc" with a subtitle saying each equals a real moc twin in its parity test and failed against a twin broken on purpose. Citation footer: wro.cpp, 2026-11-05.

## Suggested post time
Thursday 2026-11-05, 16:00 UTC
Reason: the second slot of the day, a week after the matrix post, with the three rows merged.
