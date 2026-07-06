# reflect_dx: auto-generated debugger pretty-printers + docs from struct shape

## Body
Every C++ shop maintains `.natvis` files for Visual Studio, LLDB scripts for Xcode, GDB pretty-printers for Linux. They are written by hand. They go stale. Every C++ shop wishes their headers were documented but cannot face Doxygen XML. C++26 reflection collapses both into a build-step:

```bash
$ reflect_dx --emit natvis include/User.hpp > User.natvis
$ reflect_dx --emit lldb  include/User.hpp > .lldbinit
$ reflect_dx --emit md    include/User.hpp > docs/User.md
```

Each emitter walks the header's reflected types and produces the format the corresponding tool consumes. natvis output for `struct User`:

```xml
<Type Name="User">
  <DisplayString>{name={name} age={age} admin={admin} home={home}}</DisplayString>
  <Expand>
    <Item Name="name">name</Item>
    <Item Name="age">age</Item>
    <Item Name="admin">admin</Item>
    <Item Name="home">home</Item>
  </Expand>
</Type>
```

Add a member to `User`, the natvis updates on next build. Rename a member, the visualiser renames. Remove the struct, the entry vanishes. **Your struct IS your debugger visualisation; your struct IS your generated docs.** No parallel artefact to maintain; no stale .natvis to ship and embarrass yourself with on the next demo.

What this REPLACES: hand-written `.natvis` per project, custom `~/.lldbinit` formatters per type, the half-finished `docs/types.md` that never got written. The build-step pattern means CI guarantees the artefacts match the headers.

What this does NOT replace: domain-specific visualisers (a `Quaternion` that should display as Euler angles, a `Color` that should show a swatch, a `Bitmap` that should render a thumbnail). Those still need a manual specialisation. The default exists for the common case: structural display matching the field layout, kept in sync with the struct.

The same `nonstatic_data_members_of` walker drives every emit format in the reflection arc: print, JSON, LLM schema, lens, generator, natvis. Six destinations, one walker.

Series post 22 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with clang-p2996.

https://wrocpp.github.io/posts/reflect-dx/

## Hashtags
#cpp #cpp26 #reflection #natvis #lldb #gdb #debugger #docs #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_dx". Subhead: auto-generated natvis / LLDB / GDB pretty-printers + markdown docs from struct shape; build-step pattern. Citation: wro.cpp 2026-06-23.

## Suggested post time
Tuesday 2026-06-23, 10:00 CET
Reason: Tuesday morning EU C++ + DX-tooling audience; reflection-arc post 22 continues the every-2-day cadence.
