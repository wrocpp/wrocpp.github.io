# Four range views headed for the standard library

## Body
std::ranges shipped in C++20 with a long tail of missing views that everyone fills the same way. The 2026-07 mailing closes four of them, all from Hewill Kang: views::unique (drop adjacent duplicates), views::take_last and views::drop_last (the last n, or all but the last n), and views::cycle (repeat a range endlessly).

None ship yet, so the demo shows what you write today to get each result: unique is chunk_by then take one each, take_last(3) is drop(size - 3), cycle is repeat plus join plus take. Each works and each is easy to get slightly wrong. The proposed views are more readable and, for take_last and cycle, safer.

https://wrocpp.github.io/posts/ranges-views-wave/

## Hashtags
#cpp #cplusplus #ranges #stl #programming

## Alt-text
A cream wro.cpp social card reading "Four range views you keep hand-rolling", about proposed views::unique, take_last, drop_last, and cycle.

## Suggested post time
Wednesday 2026-08-12, 10:00 CET
Reason: midweek mid-morning CET for the EU audience.
