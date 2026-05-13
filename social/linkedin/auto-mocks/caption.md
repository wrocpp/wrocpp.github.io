# Reflection-driven mocks: interface -> test double in 50 lines

## Body
GoogleMock-style mocks require a `MOCK_METHOD0(now, int())` line per method per interface. Mechanical boilerplate that follows from the interface shape -- which means reflection can write it. Walk the interface's virtual functions, emit a class that implements each with a recording stub + an expectation-setting API.

```cpp
struct IClock {
    virtual int          now()  = 0;
    virtual std::string  zone() = 0;
    virtual ~IClock() = default;
};

auto mock = mocks::make<IClock>();    // reflection-generated derived class
mock.now_returns(42);
mock.zone_returns("Europe/Warsaw");

std::println("now:  {}", mock.now());   // 42
std::println("zone: {}", mock.zone());  // Europe/Warsaw
std::println("now:  {}", mock.now());   // 42
mock.verify();
// IClock::now called 2 times
// IClock::zone called 1 times
```

Implementation walks `members_of(^^IClock)` filtered by `is_virtual()` and emits the override + per-method counter + per-method returns-this-value setter. The reflection-series post covers the full ~50 lines of header.

What reflection-alone gives you: per-method call counting, fixed return values, the basic GMock surface. What it does NOT cover: argument matchers (`Eq(42)`, `_`, `AnyOf(...)`), sequenced expectations (`InSequence`), per-call actions (`.WillOnce(Return(...))`). Those want C++29 token injection (P3294) to synthesise the matcher dispatch + action wiring -- a thin reflection-driven wrapper over std::function members can't match GMock's full expressiveness today.

For the 80% of mocks that are "this method should be called N times and return X", reflection-only is enough. For the remaining 20%, stay with GoogleMock or Trompeloeil until C++29 lands.

Cross-link: post 24 (`reflect-tracing`) uses the same walker pattern for auto-instrumentation in profilers.

Series post 15 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/auto-mocks/

## Hashtags
#cpp #cpp26 #reflection #mocking #testing #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Reflection-driven mocks: interface to test double in 50 lines". Subhead: walk virtual methods, emit recording stubs + verify(). Citation: wro.cpp 2026-06-03.

## Suggested post time
Wednesday 2026-06-03, 10:00 CET
Reason: Mid-week morning slot; reflection-arc post 15 continues the 2-day cadence.
