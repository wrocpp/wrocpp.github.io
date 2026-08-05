# std::indirect makes PImpl copyable without writing a copy constructor

## Body
PImpl with unique_ptr works, at the cost of three irritations that have nothing to do with the idea.

unique_ptr is move-only, so a copyable class needs a hand-written copy constructor and copy assignment that allocate a new Impl and copy it. The destructor has to be defined in the translation unit where Impl is complete, so you declare it in the header and default it in the source, forever. And const does not propagate: in a const member function the pointer is const, not the pointee, so a const method can mutate the implementation and the compiler will not object.

C++26 adds the type that removes all three. std::indirect is not a smart pointer, it is an indirect value: the object it refers to is part of the value, so copying copies deeply, const propagates through, and it is never null except after a move.

The demo copies a Widget, mutates the copy, and shows the original untouched, with no user-declared copy constructor, no copy assignment and no out-of-line destructor. All five special members are implicit.

It comes with std::polymorphic, which copies the dynamic type through a base pointer, so a polymorphic<Shape> holding a Circle copies a Circle. That is the old "value semantics for a class hierarchy" problem, solved without a clone() on every derived class.

Both are in GCC 16.1 today: https://wrocpp.github.io/posts/std-indirect-pimpl/

How much PImpl boilerplate would this delete from your codebase?

## Hashtags
#cpp #cplusplus #cpp26 #stdlib #softwaredesign #programming

## Alt-text
A cream wro.cpp social card reading "PImpl without writing a copy constructor", about C++26 std::indirect.

## Suggested post time
Sunday 2026-08-09, 10:00 CET
Reason: weekend mid-morning for a design-focused read.
