# Reading a signal-to-slot wiring table from annotations on the slots

## Body
Leonardo Rossi wrote a LinkedIn post on a clean way to wire signals to slots: a class lists its connections once, as a tuple of pairs of member pointers, and one function connects or disconnects all of them. I asked whether the list can sit on the slots instead.

On GCC 16.2 it can. Three annotations on the slots replace the tuple of three pairs, reflection collects them into a table, and template for connects or disconnects each edge. A static_assert over the table catches a slot with other argument types than the signal, an annotation that names something that is not a signal of Step, and a repeated edge. The same source also built on GCC trunk and on the Bloomberg clang fork.

The tuple is not the loser. It is 17 lines against 59 for the reusable annotated part, it needs no checks because the member pointers are typed, and it works in C++17 with Qt today. The signal type in my example is a small one of my own: this is not Qt, and I did not run Qt's connect. An annotation is also checked only when something walks it.

https://wrocpp.github.io/posts/wiring-table-on-the-slots/

## Hashtags
#cpp #cpp26 #reflection #annotations #qt #signals #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Put the wiring table on the slots" with a subtitle about three annotations replacing a tuple of three pairs, a static_assert on the table, and a signal type that is not Qt. Citation footer: wro.cpp, 2026-12-24.

## Suggested post time
Thursday 2026-12-24, 08:00 UTC
Reason: the morning slot on the publication day; the second post of a pair on a LinkedIn post about fold expressions and signal wiring, after the one of 23 December.
