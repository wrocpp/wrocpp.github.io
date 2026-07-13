# Copying a pmr::vector silently drops its allocator

## Body
A pmr::vector<int> looks like a value. It compares element by element, prints like a vector, and b = a compiles without a murmur. Then you check where b's memory lives, and it is not where a's is.

In the demo, original allocates from a stack arena. copy is copy-constructed from it and compares equal. But copy does not use the arena. It fell back to the default resource, the global heap, and nothing warned you.

The reason is select_on_container_copy_construction: for polymorphic_allocator it returns a default-constructed allocator rather than a copy of the source's. The standard treats the resource as salient state, the identity of an arena, which a copy should not silently inherit. So a copied container lands on the default heap unless you name the resource at the copy site.

The three propagation traits are all false for polymorphic_allocator, so the allocator is sticky: it stays with the object it was born on. A pmr::vector is a container with an identity, not a bag of values you can freely duplicate and expect the memory to follow. The fix is easy once you know the shape. The bug is that nothing makes you.

Episode 4 of the pmr series.

https://wrocpp.github.io/posts/pmr-not-a-value-type/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #memory #allocators #moderncpp

## Alt-text
A cream wro.cpp card reading "Your pmr::vector is not a value type", on pmr copy semantics.

## Suggested post time
Wednesday 2026-09-02, 10:00 CET
Reason: midweek morning CET; matches the series cadence.
