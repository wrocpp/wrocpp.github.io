# reflect_tracing

## Body
~200 ns per span, function-address payload, Chrome / Perfetto JSON dump. Engine: Maciek Gajewski's 2021 wro.cpp technique. Reflection contributes the instrumentation layer (function name, signature, source location) without `__PRETTY_FUNCTION__` macros. Today: one scope-guard per function. Tomorrow (C++29): `[[trace]]` annotation makes it invisible.

Series post 24 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/reflect-tracing/

## Hashtags
#cpp #cpp26 #reflection #tracing #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "reflect_tracing". Subhead: ~200 ns per span + Chrome/Perfetto dump. Citation: wro.cpp 2026-06-27.

## Suggested post time
Saturday 2026-06-27, 10:00 CET
Reason: Saturday morning EU audience.
