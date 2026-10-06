# Reporting, reordering and budgeting struct padding with reflection

## Body
Four fields take 32 bytes in one order and 24 in another. The post builds a C++26 reflection toolkit that reports the padding, reorders the type and fails the build over a budget, then measures whether it is faster: a modest, noisy 0.84 to 0.87 times in one streaming pass at 10 million elements, and nothing in a branchy pass. GCC 16.2 only, and the post lists what was not tested.

https://wrocpp.github.io/posts/struct-layout-toolkit-reflection/

## Hashtags
#cpp #cpp26 #reflection #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Four fields, 32 bytes or 24. Does the order change the speed?" with a subtitle saying that a reflection toolkit reports the padding, reorders the type and budgets it, and that the measured gain is one streaming pass on one machine. Citation footer: wro.cpp, 2026-11-14.

## Suggested post time
Saturday 2026-11-14, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
