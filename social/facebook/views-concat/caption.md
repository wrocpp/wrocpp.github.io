# views::concat iterates several containers as one range

## Body
Walking several containers as if they were one had no good answer before C++26. You copied everything into a scratch vector, wrote the loop three times, or hand-rolled iterators, and none of it composed with ranges.

std::views::concat presents any number of ranges as a single sequence, borrowing rather than copying. The demo joins a vector, an array, and another vector, then pipes the result through transform. Each container keeps its own storage and its own type.

The difference from join matters: join flattens a range of ranges, all the same type. concat takes the ranges as separate arguments, and they can be different types as long as their elements share a common reference type. A vector, an array, and a span are unrelated types, so join cannot help and concat takes them as they are.

Shipping in GCC 16.1: https://wrocpp.github.io/posts/views-concat/

## Hashtags
#cpp #cplusplus #cpp26 #ranges #programming

## Alt-text
A cream wro.cpp social card reading "Three containers, one range, no copy", about C++26 views::concat.

## Suggested post time
Wednesday 2026-09-09, 10:00 CET
Reason: midweek mid-morning CET for the EU audience.
