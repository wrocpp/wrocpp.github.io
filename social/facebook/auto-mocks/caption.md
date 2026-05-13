# Reflection-driven mocks

## Body
GoogleMock requires `MOCK_METHOD` per interface method. Reflection walks virtual methods of an interface and emits the test double automatically: per-method call counters, per-method returns-this-value setters, `verify()` reports call counts.

Covers the 80% case (call counting + fixed returns). The remaining 20% (argument matchers, sequences, actions) wants C++29 token injection.

Series post 15 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/auto-mocks/

## Hashtags
#cpp #cpp26 #reflection #mocking #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Reflection-driven mocks: interface to test double". Subhead: walk virtual methods, emit recording stubs + verify(). Citation: wro.cpp 2026-06-03.

## Suggested post time
Wednesday 2026-06-03, 10:00 CET
Reason: Mid-week morning slot for EU C++ audience.
