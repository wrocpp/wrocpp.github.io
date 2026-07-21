# std::inplace_vector is a vector that never touches the heap

## Body
There has always been a gap between std::array and std::vector. Array is fixed-size with no push_back. Vector is dynamic but pays for it with a heap allocation you cannot always afford, in an interrupt handler, an audio callback, or a hot loop. For decades the answer was a hand-rolled static vector: a raw buffer plus a count. Every serious codebase has one.

C++26 puts it in the standard library as std::inplace_vector<T, N>. It is a contiguous sequence container with a dynamic size up to a compile-time capacity N, and its storage lives inline, inside the object. No allocator, no heap, ever. The demo fills an inplace_vector<int, 4> to capacity and prints it, all on the stack.

Because capacity is bounded, it answers a question vector never faces: what happens when you push past N. push_back throws bad_alloc, keeping the familiar interface. try_push_back does not throw, it reports the failure so the full case is an ordinary branch, which is what you want where exceptions are banned. There is also unchecked_push_back for when you have already proven there is room.

The obvious audience is embedded and real-time, but a small known-bounded collection is clearer as an inplace_vector than as a vector you immediately reserve. GCC 16.1 ships it now: https://wrocpp.github.io/posts/inplace-vector/

Which of your hand-rolled static vectors can retire?

## Hashtags
#cpp #cplusplus #cpp26 #embedded #performance #stl #programming

## Alt-text
A cream wro.cpp social card reading "A vector that never touches the heap", about C++26 std::inplace_vector with compile-time capacity and inline storage.

## Suggested post time
Friday 2026-07-31, 10:00 CET
Reason: Friday mid-morning CET for the EU audience heading into the weekend reading slot.
