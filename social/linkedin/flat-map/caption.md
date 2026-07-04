# std::flat_map is just two vectors, and that is the point

## Body
C++23's std::flat_map keeps making the rounds as "a faster std::map". True -- but the pitch hides the design, and the design tells you when it fits.

flat_map is not a tree at all. It is an adaptor over TWO sequences: a sorted vector of keys and a parallel vector of values. The API does not pretend otherwise: keys() and values() hand you the underlying containers, and std::sorted_unique + two moved-in vectors builds the map by adopting your data with zero sorting work. Our demo makes the layout visible in three println calls, and it runs live on Compiler Explorer (GCC 16.1 and clang/libc++ both ship it).

What the two vectors buy: cache-friendly binary search instead of pointer chasing, no per-node allocation, free bulk construction.

What they cost (the part the hype skips): O(n) insertion into a populated map, iterator AND reference invalidation on every insert/erase, and an unusual exception contract -- a throwing mutation may restore invariants by clearing the container.

And one framing fix: flat_map competes with std::map, not std::unordered_map. A good hash table still wins pure point lookups; flat_map wins ordered iteration and memory.

Demo + full tradeoffs: https://wrocpp.github.io/posts/flat-map/ -- have you replaced a tree with contiguous storage and measured it?

## Hashtags
#cpp #cplusplus #cpp23 #stl #performance #datastructures #flatmap

## Alt-text
A cream wro.cpp-branded social card titled "std::flat_map is just two vectors" with a sub-claim about cache-friendly lookups, O(n) insertion, and replacing std::map rather than unordered_map.

## Suggested post time
Saturday 2026-07-18, 10:00 CET
Reason: post lands on its own pubDate; mid-morning CET for the EU C++ audience.
