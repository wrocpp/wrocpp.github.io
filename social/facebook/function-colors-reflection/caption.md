# Define your own function colors

## Body
"What color is your function?" is a decade-old complaint about async/await splitting code into async and sync halves. But C++ has had colored functions for years: consteval, CUDA's __device__, Clang's [[clang::nonblocking]] all restrict who can call what. Each one needed a compiler change.

C++26 reflection lets you define your own. std::meta::current_function() hands a callee the reflection of its caller at compile time, so in about 20 lines you can build audio-thread safety, capability tokens, or architectural-layer checks that refuse to compile when called from the wrong place.

Five runnable GCC 16 examples, plus an honest look at where the trick breaks.

https://wrocpp.github.io/posts/function-colors-reflection/

## Hashtags
#cpp #cpp26 #reflection #metaprogramming #functioncoloring

## Alt-text
Dark wro.cpp social card. Headline "Define your own function colors" with the line "C++26 reflection lets a callee inspect and reject its caller at compile time."

## Suggested post time
2026-06-22, 10:00 CET
Reason: matches the 08:00 UTC publish slot; mid-morning CET catches the EU C++ audience.
