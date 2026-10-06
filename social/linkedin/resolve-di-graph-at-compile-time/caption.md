# C++26 reflection resolves a dependency-injection graph at compile time

## Body
A constructor's parameter list is enough to wire an application. In C++26 you can read that list at compile time.

I put a 231-line header on it. It calls parameters_of on each constructor, plans the whole object graph in one consteval function, and stores the objects in a struct built by define_aggregate. A cycle stops the build with "dependency cycle: A -> B -> C -> A". A missing or ambiguous binding does the same, naming the parameter and the path.

Against hand wiring on GCC 16.2, the generated code makes the same calls only with exceptions off (and uninitialized stack storage). With exceptions on, the graph carries extra cleanup code and I did not find out why. A 300-type graph needs -fconstexpr-ops-limit=4000000000 and compiles in about 5 seconds on an M2 Max. By-value parameters are refused.

Boost.DI is the baseline and has years of production use that this does not. The post also corrects what my earlier dependency-injection post got wrong, and ends with what I have not tested.

https://wrocpp.github.io/posts/resolve-di-graph-at-compile-time/

## Hashtags
#cpp #cpp26 #reflection #dependencyinjection #gcc #templates

## Alt-text
Dark card with the headline "Your compiler can wire the dependencies" and a line about a 231-line C++26 header that plans an object graph at compile time.

## Suggested post time
Wednesday 2026-11-11, 10:00 CET
Reason: midweek morning slot, same as the series' other flagship posts.
