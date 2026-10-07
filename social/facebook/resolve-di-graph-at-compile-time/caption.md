# C++26 reflection resolves a dependency-injection graph at compile time

## Body
Your constructors already say what depends on what. C++26 reflection can read that at compile time.

A 231-line header plans the whole object graph before the program runs. A cycle, a missing binding or an ambiguous one stops the build with a sentence naming the path. With exceptions off, GCC 16.2 compiles it to the same calls as hand wiring. With exceptions on it does not, and I do not know why yet.

The post covers the limits too: a 300-type graph needs a raised constexpr limit, and by-value parameters are refused.

https://wrocpp.github.io/posts/resolve-di-graph-at-compile-time/

## Hashtags
#cpp #cpp26 #reflection #dependencyinjection #gcc

## Alt-text
Dark card with the headline "Your compiler can wire the dependencies" and a line about a 231-line C++26 header that plans an object graph at compile time.

## Suggested post time
Wednesday 2026-11-11, 10:00 CET
Reason: same slot as the LinkedIn post.
