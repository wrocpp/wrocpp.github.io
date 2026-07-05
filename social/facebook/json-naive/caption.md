# A 40-line JSON serializer in C++26

## Body
JSON serialization in C++ was either heavy (`nlohmann/json`) or hand-rolled. C++26 reflection turns it into 40 lines that walk any aggregate, emit `{key:value}` pairs, nest structs, arrayify vectors. Schema is the spec; add a field, the JSON follows.

Not a Glaze replacement. That's already on P2996 and faster than serde_json. This is the teaching version for understanding what a serializer is, and the right size for the internal-only schemas where it's enough.

Series post 8 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/json-naive/

## Hashtags
#cpp #cpp26 #reflection #json #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "A 40-line JSON serializer in C++26". Subhead: One template walks any aggregate; arrays nest, vectors arrayify. Citation: wro.cpp 2026-05-11.

## Suggested post time
Monday 2026-05-11, 18:00 CET (recovery slot)
Reason: Original morning slot missed; afternoon recovery for EU audience.
