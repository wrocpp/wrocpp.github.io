# std::osyncstream makes concurrent output atomic

## Body
Three threads logging to std::cout tear each other's lines apart. C++20 fixes it with one wrapper: std::osyncstream.

Each thread writes into its own osyncstream(std::cout). The text buffers privately and only reaches the real stream as one atomic block when the osyncstream is destroyed. Same three threads, and now every line is whole.

The catch: the guarantee holds only if every writer uses a syncstream. One raw cout alongside them can still cut in.

Episode 2 of a series on concurrent I/O.

https://wrocpp.github.io/posts/osyncstream/

## Hashtags
#cpp #cplusplus #cpp20 #concurrency #programming
