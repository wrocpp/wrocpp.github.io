# Dependency injection without the framework: reflection-driven autowiring

## Body
Spring / Guice / Dagger / Hilt all solve the same problem in JVM-land: tell the container which constructor parameter is which dependency, and let it wire the graph. C++ has historically gone two routes -- a heavy DI framework (Hypodermic, Boost.DI) with macro registration, or hand-wired factories that nobody wants to refactor.

C++26 reflection gives you the autowiring story without the framework. Walk a class's constructor parameters at compile time, look up each parameter's type in a registry, instantiate.

```cpp
struct Clock { virtual int now() = 0; };
struct Logger { virtual void log(std::string_view) = 0; };

struct Greeter {
    Greeter(Clock& c, Logger& l) : clock(c), log(l) {}
    void say_hello() { log.log(std::format("Hello @tick={}", clock.now())); }
private:
    Clock& clock;
    Logger& log;
};

// Container holds singletons keyed by type-reflection.
di::container c;
c.bind<Clock,  TickingClock>();
c.bind<Logger, StdoutLogger>();
auto& greeter = c.make<Greeter>();        // walks Greeter's ctor params via reflection
greeter.say_hello();                       // Hello @tick=1
greeter.say_hello();                       // Hello @tick=2
```

The `make<T>()` call walks T's constructor parameters using `parameters_of(^^T::T)`, looks up each type in the container, and constructs. No `@Inject` annotations, no codegen step, no XML config. The reflection-driven version handles the four-line case in ten lines of header.

What this does NOT replace: full DI frameworks with lifecycle scopes (request / session / singleton), conditional bindings, AOP interception. The lightweight version covers the common case where you've been doing manual factory wiring -- a `Greeter` that needs `Clock` and `Logger`, and a test that wants to swap in mocks.

Series post 14 of 25 in the wro.cpp C++26 reflection arc. Cross-link with post 15 (auto-mocks) which produces interface test doubles for the same pattern.

https://wrocpp.github.io/posts/dependency-injection/

## Hashtags
#cpp #cpp26 #reflection #di #dependencyinjection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Dependency injection without the framework". Subhead: reflection walks constructor parameters at compile time; container.make<T>() wires the graph. Citation: wro.cpp 2026-05-30.

## Suggested post time
Saturday 2026-05-30, 10:00 CET
Reason: Saturday morning slot catches weekend reading-list builders; reflection-arc post 14 continues the 2-day cadence.
