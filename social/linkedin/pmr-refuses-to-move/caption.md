# Move-assigning pmr containers across arenas deep-copies

## Body
Move assignment is supposed to be the cheap one. dst = std::move(src) steals the source's buffer, leaves it empty, and touches no elements. For two pmr containers with different resources, that steal is impossible, and the standard quietly does the expensive thing.

In the demo, src holds a hundred ints in one arena and dst uses another. After dst = std::move(src), dst has the hundred elements, and its resource performed one allocation to hold them. A genuine move allocates nothing. This one copied every element into fresh storage.

The reason is ownership. src's buffer belongs to src's arena. If dst stole the pointer, it would later free that memory into its own resource, which never owned it, and that is corruption. So when propagate_on_container_move_assignment is false and the allocators are not equal, move assignment allocates in the destination and moves elements one at a time. An O(1) operation becomes O(n), silently, on a runtime property the type system cannot see.

Within one resource, move is still O(1). Across resources it turns into a copy you did not write. Reach for pmr where the arenas are stable and shared, and be deliberate about moving containers between them.

Episode 5 of the pmr series.

https://wrocpp.github.io/posts/pmr-refuses-to-move/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #memory #performance #moderncpp

## Alt-text
A cream wro.cpp card reading "The allocator that refuses to move", on pmr move semantics.

## Suggested post time
Wednesday 2026-09-16, 10:00 CET
Reason: midweek morning CET; matches the series cadence.
