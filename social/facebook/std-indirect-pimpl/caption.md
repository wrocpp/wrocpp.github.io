# std::indirect makes PImpl copyable without writing a copy constructor

## Body
PImpl with unique_ptr works, at the cost of three irritations unrelated to the idea. unique_ptr is move-only, so you hand-write copy operations. The destructor must be defined where Impl is complete. And const does not propagate, so a const method can still mutate the implementation.

C++26's std::indirect removes all three. It is not a smart pointer but an indirect value: copying copies deeply, const propagates through, and it is never null except after a move. All five special members can be defaulted.

It ships with std::polymorphic, which copies the dynamic type through a base pointer, solving the old "value semantics for a hierarchy" problem without a clone() on every derived class.

Both are in GCC 16.1: https://wrocpp.github.io/posts/std-indirect-pimpl/

## Hashtags
#cpp #cplusplus #cpp26 #softwaredesign #programming

## Alt-text
A cream wro.cpp social card reading "PImpl without writing a copy constructor", about C++26 std::indirect.

## Suggested post time
Sunday 2026-08-09, 10:00 CET
Reason: weekend mid-morning for a design read.
