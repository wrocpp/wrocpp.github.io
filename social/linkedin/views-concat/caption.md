# views::concat iterates several containers as one range

## Body
Iterating several containers as if they were one is an ordinary need with no good answer before C++26. You copied everything into a scratch vector, which allocates and duplicates the data, or you wrote the loop three times, or you hand-rolled a nest of iterators. None of it composed with the rest of ranges.

std::views::concat is the missing adaptor. It presents any number of ranges as a single sequence, borrowing rather than copying. The demo joins a vector, an array, and another vector, then pipes the result through transform. The three containers keep their own storage and their own types, and nothing was copied to produce the view.

The distinction from join is the useful part:

  views::join flattens a range OF ranges, one container whose elements are containers, all the same type.
  views::concat takes several ranges as separate arguments, and they may be different types as long as the elements share a common reference type.

That is what makes concat work on real code. A vector and an array and a span are unrelated types; join cannot help, because you cannot put them in one container without erasing something. concat takes them as they are.

The view is as capable as its weakest input: random access and sizing survive when every input supports them, which is why ranges::size works in the demo.

Typical uses look exactly like what it says: a default set followed by user overrides, several buckets walked in order, a header and a body run through one algorithm without merging them first.

Shipping in GCC 16.1: https://wrocpp.github.io/posts/views-concat/

Which range adaptor do you still find yourself hand-rolling?

## Hashtags
#cpp #cplusplus #cpp26 #ranges #stl #programming

## Alt-text
A cream wro.cpp social card reading "Three containers, one range, no copy", about C++26 views::concat.

## Suggested post time
Wednesday 2026-09-09, 10:00 CET
Reason: midweek mid-morning CET for the EU audience.
