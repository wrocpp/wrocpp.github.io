# std::inplace_vector is a vector that never touches the heap

## Body
There has always been a gap between std::array (fixed size, no push_back) and std::vector (dynamic, but it allocates). For decades the answer was a hand-rolled static vector: a buffer plus a count. Every serious codebase has one.

C++26 puts it in the standard library as std::inplace_vector<T, N>: a dynamic size up to a compile-time capacity, with storage held inline in the object. No allocator, no heap. push_back throws when full, or use try_push_back to get a plain branch instead of an exception.

The audience is embedded and real-time, but any small bounded collection is clearer this way. GCC 16.1 ships it now: https://wrocpp.github.io/posts/inplace-vector/

## Hashtags
#cpp #cplusplus #cpp26 #embedded #programming

## Alt-text
A cream wro.cpp social card reading "A vector that never touches the heap", about C++26 std::inplace_vector.

## Suggested post time
Friday 2026-07-31, 10:00 CET
Reason: Friday mid-morning CET for the EU audience.
