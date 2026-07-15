# Your std::cout logging has no data race and still tears

## Body
Qt calls a log handler from several threads at once (its docs require the handler to be reentrant). Point that handler at std::cout and the output tears: three threads writing lines, and the records splice into each other mid-line.

It is not undefined behavior. The C++ standard guarantees concurrent use of a synchronized cout has no data race. It just does not guarantee the characters stay apart. Each << is its own operation, so another thread can cut in between them. No data race, but a race condition all the same.

That gap is what osyncstream (C++20) and std::print (C++23) exist to close.

Episode 1 of a new series on concurrent I/O.

https://wrocpp.github.io/posts/logs-race-free-but-garbled/

## Hashtags
#cpp #cplusplus #cpp20 #concurrency #programming
