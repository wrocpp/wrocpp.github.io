# Replacing Qt's MOC with C++26 reflection -- no second compiler, no .moc files

## Body
Qt's Meta-Object Compiler is one of the oldest codegen tools in C++ -- it parses headers looking for `Q_OBJECT`, `Q_PROPERTY`, `Q_INVOKABLE`, `signals:`, `slots:` and emits glue code that adds runtime introspection, property binding, and QML integration. It works. It also means Qt projects ship a second compiler, every IDE needs MOC awareness, and your headers have a parallel syntax that isn't quite C++.

C++26 reflection collapses the `Q_PROPERTY` half of MOC into a regular library:

```cpp
struct User {
    [[=rqt::property{}]]                      std::string name = "Filip";
    [[=rqt::property{}]]                      int         age  = 40;
    [[=rqt::property{}, =rqt::read_only{}]]   std::string id   = "u-0001";
};

auto props = rqt::properties_of<User>();
// runtime registry built from reflection: name/type/read-only flag +
// type-erased getter and setter for each property
```

The trick: walk `nonstatic_data_members_of(^^T)` at compile time, filter by P3394 annotations, build per-member getter/setter closures via templated helpers (regular lambdas can't capture template-for-introduced variables; templated helpers with the pointer-to-member as a NTTP sidestep the rule). The resulting `property_info` list is the same shape Qt's MOC emits as a static table -- just generated from the language, not a separate parser.

What this REPLACES: `Q_PROPERTY`, the .moc compilation step, the IDE plugins that have to keep up with MOC syntax, and the discipline of remembering to add a property to the macro list when you add a member.

What this does NOT replace: `signals`/`slots` (signal connection still benefits from MOC's connection-graph machinery), QML integration (Qt's QML engine reads MOC tables; libraries like rqt would need to register themselves with that engine), thread-affinity policy (`QObject::moveToThread`). Those are framework concerns; MOC's metadata-emit half is just one slice.

Series post 17 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996 (`-std=c++26 -freflection-latest -stdlib=libc++`).

https://wrocpp.github.io/posts/qt-moc-replacement/

## Hashtags
#cpp #cpp26 #reflection #qt #moc #qml #properties #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Replacing Qt's MOC with reflection". Subhead: P3394 annotations + nonstatic_data_members_of replace the Q_PROPERTY-emit half of Qt's Meta-Object Compiler. Citation: wro.cpp 2026-06-11.

## Suggested post time
Thursday 2026-06-11, 10:00 CET
Reason: Mid-week morning slot reaches EU C++ + Qt engineers in flow. Reflection-arc post 17 continues the every-2-day cadence past the headline 16-post run.
