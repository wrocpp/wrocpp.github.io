# std::flat_map is just two vectors, and that is the point

## Body
C++23's std::flat_map is not a tree with better marketing. It is two vectors: sorted keys and parallel values. That buys cache-friendly lookups and zero memory overhead per node -- and costs O(n) insertion and aggressive iterator invalidation.

Our runnable demo makes the layout visible: keys() prints the sorted array, values() the parallel one, and sorted_unique adopts your pre-sorted data with no work at all. Runs live in your browser.

The framing fix most posts skip: flat_map replaces std::map, not std::unordered_map.

Read it: https://wrocpp.github.io/posts/flat-map/

## Hashtags
#cpp #cplusplus #cpp23 #stl #performance

## Alt-text
A cream wro.cpp-branded social card titled "std::flat_map is just two vectors" with a sub-claim about cache-friendly lookups, O(n) insertion, and replacing std::map rather than unordered_map.

## Suggested post time
Saturday 2026-07-18, 10:00 CET
Reason: post lands on its own pubDate; mid-morning CET for the EU C++ audience.
