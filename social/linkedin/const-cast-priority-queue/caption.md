# You cannot move out of a priority_queue without a const_cast

## Body
std::priority_queue is a heap, and a heap is only a heap while its ordering invariant holds. If you could mutate the top element in place you could change the key the heap is organised by, so top() returns a const reference. That is a sound decision.

It also means you cannot get a move-only element back out. Task t = pq.top() selects the copy constructor, and if Task holds a unique_ptr there is no copy constructor to select, so the line does not compile. There is no extract() on priority_queue the way there is on the associative containers, and no move-aware pop().

The accepted workaround is to cast the const away, and it is worth being precise about why that is defensible. const_cast is undefined behavior only when you modify an object originally declared const. The elements inside the queue's underlying vector are not const objects; top() merely hands you a const view of them. Removing that view's constness is legal.

What makes it safe rather than merely legal is the next line:

  Task t = std::move(const_cast<Task&>(pq.top()));
  pq.pop();

After the move the top element is valid but unspecified, which would be a real problem if the heap ever compared it again. pop() destroys it first. The two lines are effectively one operation, and anything inserted between them is a bug: an early return, a continue, or a throw leaves a moved-from element at the root of the heap.

If that makes you uncomfortable, use a vector with make_heap and pop_heap. Same algorithm, no cast.

https://wrocpp.github.io/posts/const-cast-priority-queue/

## Hashtags
#cpp #cplusplus #stl #movesemantics #programming

## Alt-text
A cream wro.cpp social card reading "priority_queue will not let go of your object", about const_cast and move-only elements.

## Suggested post time
Tuesday 2026-08-18, 10:00 CET
Reason: Tuesday mid-morning CET, a strong weekday slot.
