# Derive eq + hash from struct shape

## Body
C++20's `operator==() = default` covers two-thirds of what value types need; `std::hash<T>` is still hand-written. C++26 reflection fills the gap: one header walks any aggregate and emits hash + per-field-annotated equality (epsilon for floats, skip flags, normalise-first). Schema-as-spec for value semantics.

Series post 7 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt.

https://wrocpp.github.io/posts/derive-eq-hash/

## Hashtags
#cpp #cpp26 #reflection #hash #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Derive eq + hash + ordering from struct shape". Subhead: Reflection fills the std::hash gap with per-field annotations for epsilon, normalisation, skip. Citation: wro.cpp 2026-05-09.

## Suggested post time
Saturday 2026-05-09, 10:00 CET
Reason: Saturday morning slot for EU C++ audience.
