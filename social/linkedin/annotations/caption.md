# Annotations: the serde-parity feature C++26 actually shipped

## Body
Rust's serde gives you per-field attributes (`#[serde(rename = "id")]`, `#[serde(skip)]`, `#[serde(default)]`) declaratively wired into derive macros. C++ until 2026 either generated this from a separate DSL (protobuf .proto, Cap'n Proto schemas) or wrote it by hand per field per direction.

P3394 (user-defined annotations), adopted into C++26 alongside P2996 reflection, closes the gap. Annotation values are arbitrary constant expressions; `std::meta::annotations_of(reflection)` reads them back at compile time. The JSON walker from post 8 grows three lines per feature:

```cpp
struct User {
    [[=json::rename{"userName"}]]            std::string name;
                                              int id;
    [[=json::default_value{"a@b.c"}]]        std::string email;
    [[=json::skip_if_empty{}]]               std::string bio;
    [[=json::rename{"isAdmin"}]]             bool admin;
};

// to_json(User{...}) ->
// {"userName":"filip","id":42,"email":"a@b.c","bio":"hello","isAdmin":true}
// to_json(User{name:"anon", id:7, email:"", bio:"", admin:false}) ->
// {"userName":"anon","id":7,"email":"a@b.c","isAdmin":false}   // bio skipped, email defaulted
```

Same per-field annotations propagate to YAML / TOML / XML walkers (post 11 demonstrates the cross-format reuse). One annotation taxonomy, every format. The serde derive-attribute parity arrives without a codegen step.

Where this matters in production: API boundary structs that you want to mark `[[=secret]]` for redaction in logs + `[[=json::skip]]` to never serialise + `[[=db::column{"password_hash"}]]` for the ORM mapping. One struct definition, four different consumers each reading its own annotations off the same reflection. The annotation IS the spec.

Series post 9 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/annotations/

## Hashtags
#cpp #cpp26 #reflection #annotations #serde #p3394 #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Annotations: serde-parity in C++26". Subhead: Per-field rename/skip/default attributes via P3394; one struct serves JSON + YAML + TOML walkers. Citation: wro.cpp 2026-05-13.

## Suggested post time
Wednesday 2026-05-13, 10:00 CET
Reason: Mid-week morning slot; reflection-arc post 9 continues the 2-day cadence.
