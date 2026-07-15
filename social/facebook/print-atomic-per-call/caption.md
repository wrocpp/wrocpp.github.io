# std::print does not tear the way std::cout does

## Body
C++23's std::print gives you what iostreams never did for free: a single print call never interleaves with another. No syncstream, no mutex, one call, one whole line. It formats into a temporary and writes it in one locked operation.

The catch is that the guarantee is per call. Build one logical line from two print calls and another thread's output can land between them. The fix: put the whole line in a single print call.

Episode 4 of a series on concurrent I/O.

https://wrocpp.github.io/posts/print-atomic-per-call/

## Hashtags
#cpp #cplusplus #cpp23 #concurrency #programming
