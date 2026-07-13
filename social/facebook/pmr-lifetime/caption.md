# The pmr crash is the buffer that died first

## Body
The most common std::pmr crash is not a bug in a custom resource. It is lifetime.

A pmr container frees its memory back into its resource when destroyed, so the resource has to outlive it. In one scope that means declaration order: declare the resource first, the container second, because destructors run in reverse. Get it backwards and the container frees memory into an object that is already gone, which is undefined behavior.

There is no borrow checker to catch it. Own the resource at least as long as everything that allocates from it.

Episode 6 of the pmr series.

https://wrocpp.github.io/posts/pmr-lifetime/

## Hashtags
#cpp #cplusplus #cpp17 #memory #programming
