# Move-assigning pmr containers across arenas deep-copies

## Body
Move assignment should be a cheap pointer steal. For two pmr containers with different resources, it cannot be.

In the demo, the source holds a hundred ints in one arena and the destination uses another. After dst = std::move(src), the destination allocated once and copied every element. A real move allocates nothing; this one did an O(n) copy, because the source's buffer belongs to an arena the destination does not own.

Within a single resource move stays O(1). Across resources, the word move stops meaning what you expect.

Episode 5 of the pmr series.

https://wrocpp.github.io/posts/pmr-refuses-to-move/

## Hashtags
#cpp #cplusplus #cpp17 #memory #programming
