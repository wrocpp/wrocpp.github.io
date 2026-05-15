# Replacing Qt's MOC with reflection

## Body
Qt's Meta-Object Compiler emits glue code for `Q_PROPERTY` / `Q_INVOKABLE` / `signals` / `slots`. Project ships a second compiler, IDEs need MOC awareness, headers carry near-but-not-quite-C++ syntax. C++26 reflection makes the property-introspection half a regular library: walk `nonstatic_data_members_of(^^T)`, filter by P3394 annotations, build a runtime registry. No .moc files, no codegen pass, no extra build step. signals/slots and QML wiring still benefit from MOC's other halves -- but the metadata emit is now just C++.

Series post 17 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/qt-moc-replacement/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Replacing Qt's MOC with reflection". Subhead: Property registry from struct shape; no .moc files, no second compiler. Citation: wro.cpp 2026-06-11.

## Suggested post time
Thursday 2026-06-11, 10:00 CET
Reason: Mid-week morning EU audience.
