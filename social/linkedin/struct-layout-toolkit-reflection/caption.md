# Reporting, reordering and budgeting struct padding with reflection

## Body
Two structs with the same four fields: one is 32 bytes, the other 24. The first has 14 bytes of padding, the second 6.

A post by Herik Lima on LinkedIn, "Cache-Friendly Structs", asked whether reorganizing struct fields ever gave a big speedup. I built a small C++26 reflection toolkit to find out what can be checked: it prints a byte map of the padding, builds a reordered copy of a type with define_aggregate, and turns a padding or hot-group budget into a static_assert that fails the build with the numbers in the message.

Three findings. Sorting by descending alignment reached the minimum size for all 2,992 small member sets I enumerated, but not for 1,578 of 11,613 once a member is over-aligned. The reordered copy is a different type in every way P1112R5 lists: designated-initialiser order, structured bindings, ordering, operator==, object representation. And the speed: on an Apple M2 Max, 0.84 to 0.87 times the time in one streaming branch-free pass at 10 million elements. At 1,000 elements the effect is gone, a branchy pass shows nothing, and the machine was noisy.

GCC 16.2 only. The post lists what was not tested and links the prior art (pahole, clang's Padding checker, Go fieldalignment, Rust, the Linux cache-line groups).

https://wrocpp.github.io/posts/struct-layout-toolkit-reflection/

## Hashtags
#cpp #cpp26 #reflection #performance #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Four fields, 32 bytes or 24. Does the order change the speed?" with a subtitle saying that a reflection toolkit reports the padding, reorders the type and budgets it, and that the measured gain is one streaming pass on one machine. Citation footer: wro.cpp, 2026-11-14.

## Suggested post time
Saturday 2026-11-14, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
