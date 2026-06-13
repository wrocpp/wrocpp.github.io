# C++ is writing down all of its undefined behavior

## Body
The structural move at WG21 Brno was not a feature -- it was a catalogue. You cannot systematically eliminate what you have not first enumerated.

P3596R3, "Undefined Behavior and IFNDR Annexes" (Berne, Doumler, Maurer, Yaghmour), adds two non-normative annexes: one catalogues every case of undefined behavior, the other every ill-formed-no-diagnostic-required corner. Each entry gets a stable name like [ub:dcl.ref], cross-linked back into the normative text.

P3100R6 (Doumler, Berne) turns the list into a program. By inspecting every "undefined" and "assume" in the working draft, the authors counted exactly 80 cases of explicit core-language UB. Sorted into ten categories, 50 are type-and-lifetime alone; the three memory-safety categories are 56 of 80, about 70 percent. When people say C++'s safety problem is a memory-safety problem, this is the receipt.

The enforcement machinery already shipped: erroneous behavior (P2795, C++26) plus contracts. P3596 is the index, P3100 is the schedule, and the target is C++29.

https://wrocpp.github.io/posts/brno-undefined-behavior/

## Hashtags
#cpp #cpp29 #wg21 #undefinedbehavior #memorysafety #moderncpp #safety #wrocpp

## Alt-text
Editorial card with headline "C++ is writing down all of its undefined behavior" and subtitle "P3596 and P3100: 80 core-language UB cases, named and scheduled to close for C++29."

## Suggested post time
2026-06-17, 10:00 CET
