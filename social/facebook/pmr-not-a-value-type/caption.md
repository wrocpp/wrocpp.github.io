# Copying a pmr::vector silently drops its allocator

## Body
A pmr::vector looks like a value type: it compares equal, it copies, it prints normally. But copy construction does not carry the allocator.

In the demo, the original draws from a stack arena. The copy compares equal to it, yet allocates from the default heap instead of the arena, and nothing warns you. select_on_container_copy_construction hands back the default resource, because the arena is treated as an identity a copy should not inherit.

The allocator is sticky. If you want the copy in the same arena, you have to name the resource yourself.

Episode 4 of the pmr series.

https://wrocpp.github.io/posts/pmr-not-a-value-type/

## Hashtags
#cpp #cplusplus #cpp17 #memory #programming
