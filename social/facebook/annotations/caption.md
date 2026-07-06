# C++26 annotations -- serde-parity arrives

## Body
Rust's serde gives you `#[serde(rename = "id")]`, `#[serde(skip)]`, `#[serde(default)]`. C++26's P3394 (user-defined annotations, adopted alongside reflection) gives you the same:

```cpp
struct User {
    [[=json::rename{"userName"}]] std::string name;
    [[=json::skip_if_empty{}]]    std::string bio;
};
```

The same annotations propagate to YAML / TOML / XML walkers. One struct serves every format. The derive-attribute parity arrives without a codegen step.

Series post 9 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/annotations/

## Hashtags
#cpp #cpp26 #reflection #annotations #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Annotations: serde-parity in C++26". Subhead: Per-field rename/skip/default attributes via P3394. Citation: wro.cpp 2026-05-13.

## Suggested post time
Wednesday 2026-05-13, 10:00 CET
Reason: Mid-week morning slot for EU C++ audience.
