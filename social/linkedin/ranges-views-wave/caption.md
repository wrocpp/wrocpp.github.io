# Four range views headed for the standard library

## Body
std::ranges shipped in C++20 with an obvious set of views and a long tail of gaps that everyone fills the same way. The 2026-07 mailing closes four of them at once, all from Hewill Kang.

views::unique (P4291) drops adjacent duplicate elements, the range-adaptor form of std::unique. views::take_last and views::drop_last (P4294) take the last n elements, or everything but the last n, the symmetric partners to take and drop. views::cycle (P3806) repeats a range endlessly.

None ship yet, so the demo shows what you write today to get each result with the adaptors that already exist. unique means chunk_by on equality then take the first of each group. take_last(3) means drop(size - 3), which forces you to know the size and reason about the underflow when the range is shorter. cycle means repeat the range and join it, then bound it with take. Each works, and each is the kind of thing you write once, get slightly wrong, and paste around.

The proposed views are more readable and, for take_last and cycle, safer: take_last(3) cannot underflow the way drop(size - 3) can. These are R0s and will move before they land, but they are small and exactly the gap-filling that tends to make it through: https://wrocpp.github.io/posts/ranges-views-wave/

Which of these four have you already hand-rolled?

## Hashtags
#cpp #cplusplus #ranges #cpp29 #stl #programming

## Alt-text
A cream wro.cpp social card reading "Four range views you keep hand-rolling", about proposed views::unique, take_last, drop_last, and cycle.

## Suggested post time
Wednesday 2026-08-12, 10:00 CET
Reason: midweek mid-morning CET for the EU C++ audience.
