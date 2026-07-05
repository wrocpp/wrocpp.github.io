# Define your own function colors

## Body
"What color is your function?" has been a complaint about async/await for a decade. It splits a codebase into red (async) and blue (sync) halves that cannot freely call each other.

But C++ has had colored functions for years. consteval, CUDA's __device__, Clang's [[clang::nonblocking]]: each is a compile-time constraint on which functions may call which. The catch: every one of them required a compiler change.

C++26 reflection changes that. std::meta::current_function() (P3795R1) returns the reflection of the *caller* when used as a default argument (the same trick std::source_location::current() uses). With it, a callee can inspect and reject its own callers at compile time, in about 20 lines of ordinary library code.

The post walks three professional uses of the same tiny guard:
- audio-thread safety (a primitive that will not compile if called from un-painted code)
- capability tokens (sign_release only from code granted the crypto capability)
- architectural layering (raw SQL only from the data layer)

Five runnable Godbolt examples, all verified on GCC 16.1. Plus an honest "where it breaks": the annotation is a promise, not a proof. For real audio work, [[clang::nonblocking]] + RealtimeSanitizer is still the production tool.

The bigger point: reflection turned a compiler feature into a library feature. A domain-specific color used to need a standards process. Now it needs an afternoon.

https://wrocpp.github.io/posts/function-colors-reflection/

## Hashtags
#cpp #cpp26 #reflection #metaprogramming #functioncoloring #cppprogramming

## Alt-text
Dark wro.cpp social card. Headline "Define your own function colors" with the line "C++26 reflection lets a callee inspect and reject its caller at compile time."

## Suggested post time
2026-06-22, 10:00 CET
Reason: matches the 08:00 UTC publish slot; mid-morning CET catches the EU C++ audience.
