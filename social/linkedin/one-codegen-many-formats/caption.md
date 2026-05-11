# One codegen, many formats: JSON, YAML, TOML, XML from one walker

## Body
By post 11 of the reflection arc, you have a JSON walker (post 8) + per-field annotations (post 9) + the inverse deserializer (post 10). The structural shape is identical for any text format: walk T's members, emit per-field key + value with the format's particular punctuation. Post 11 generalises.

One reflection-driven walker, parameterised on a "format adapter" that knows how to write a key, a value, an open-object, a close-array. Plug in different adapters; one struct definition serves four formats:

```cpp
struct User {
    [[=json::rename{"userName"}]] std::string name;
    int id;
    [[=json::rename{"homeAddress"}]] Address home;
};

User u{"filip", 42, {"Warsaw", 12345}};

write<json>(u);  // {"userName":"filip","id":42,"homeAddress":{"city":"Warsaw","postal_code":12345}}
write<yaml>(u);  // userName: filip\nid: 42\nhomeAddress:\n  city: Warsaw\n  postal_code: 12345
write<toml>(u);  // userName = "filip"\nid = 42\n[homeAddress]\ncity = "Warsaw"\npostal_code = 12345
write<xml>(u);   // <User><userName>filip</userName><id>42</id>...</User>
```

The same `[[=json::rename]]` annotation drives the renames in every format (each adapter consults the annotation it cares about; cross-format consistency falls out). Add a `[[=json::skip]]` and every format honours it. Multi-format coherence on a single struct definition was historically the killer app for codegen tools (protobuf, Cap'n Proto, Thrift); P2996 + P3394 gets you the same coverage in 80 lines of header.

What this does NOT replace: protobuf (wire-format efficiency, schema evolution rules), msgpack (binary-compact), CBOR (RFC-blessed for IoT). The format-adapter pattern is for text-format multi-output where readability matters more than wire efficiency.

Series post 11 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/one-codegen-many-formats/

## Hashtags
#cpp #cpp26 #reflection #json #yaml #toml #serialization #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "One codegen, many formats". Subhead: A single reflection-driven walker + format adapters serves JSON, YAML, TOML, XML from one struct definition. Citation: wro.cpp 2026-05-18.

## Suggested post time
Monday 2026-05-18, 10:00 CET
Reason: Monday morning launches the week; reflection-arc post 11 continues the 2-day cadence.
