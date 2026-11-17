# Reading a signal-to-slot wiring table from annotations on the slots

## Body
Leonardo Rossi's LinkedIn post lists a class's signal-to-slot connections once, as a tuple of member pointers. Can the list sit on the slots instead? On GCC 16.2 it can: 3 annotations replace a tuple of 3 pairs, and a static_assert checks the table. The tuple is shorter, 17 lines against 59, and works with Qt today. My signal type is not Qt.

https://wrocpp.github.io/posts/wiring-table-on-the-slots/

## Hashtags
#cpp #cpp26 #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Put the wiring table on the slots" with a subtitle about three annotations replacing a tuple of three pairs, a static_assert on the table, and a signal type that is not Qt. Citation footer: wro.cpp, 2026-12-24.

## Suggested post time
Thursday 2026-12-24, 08:00 UTC
Reason: the morning slot on the publication day; the second post of a pair, after the one of 23 December.
