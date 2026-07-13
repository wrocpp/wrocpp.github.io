# The pmr crash is the buffer that died first

## Body
The first std::pmr crash most people hit rarely comes from a memory resource they wrote. It is an ordering bug: the buffer a container allocates from goes out of scope while the container is still alive, or is destroyed one line too early.

A pmr container holds a pointer to its resource and calls back into it to free memory when it is destroyed. So the resource must outlive the container. In a single scope that becomes a rule about declaration order, because destructors run in reverse.

The demo declares the resource first and the vector second. At the closing brace the vector is destroyed first, deallocates into a resource that is still alive, and only then is the resource destroyed. Swap the two lines and the vector would free memory into an object whose lifetime has already ended, which is undefined behavior and usually a crash or a corrupted heap.

The dangerous version is when the resource and the container live in different places: a local monotonic_buffer_resource handed to a container stored somewhere longer-lived, or a stack buffer passed to a resource that outlives the frame. There is no borrow checker here, only the rule that the resource stays alive for every allocation and deallocation the container performs. Declare the resource first, own it at least as long as the container, and the bug never appears.

Episode 6 of the pmr series.

https://wrocpp.github.io/posts/pmr-lifetime/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #memory #lifetime #moderncpp

## Alt-text
A cream wro.cpp card reading "The resource that died too soon", on pmr lifetime rules.

## Suggested post time
Wednesday 2026-09-30, 10:00 CET
Reason: midweek morning CET; matches the series cadence.
