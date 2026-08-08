# You cannot move out of a priority_queue without a const_cast

## Body
priority_queue::top() returns a const reference, because mutating the top element could break the heap ordering. Sound decision, with a consequence: you cannot get a move-only element back out. The copy constructor gets selected, and if the element holds a unique_ptr there is no copy constructor, so it does not compile.

The workaround is a const_cast. That is legal here because the elements in the underlying vector are not const objects; top() just hands you a const view of them.

What makes it safe is the next line being pop(). After the move the element is valid but unspecified, which would matter if the heap compared it again, and pop() destroys it first. The two lines are one operation, so anything between them is a bug.

Prefer no cast at all? Use a vector with make_heap and pop_heap.

https://wrocpp.github.io/posts/const-cast-priority-queue/

## Hashtags
#cpp #cplusplus #stl #programming

## Alt-text
A cream wro.cpp social card reading "priority_queue will not let go of your object", about const_cast and move-only elements.

## Suggested post time
Tuesday 2026-08-18, 10:00 CET
Reason: Tuesday mid-morning CET for the EU audience.
