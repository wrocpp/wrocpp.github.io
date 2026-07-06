# Fertig: this is not the cast you're looking for

## Body
Andreas Fertig's 2026-05-18 post (re-shared on isocpp.org): `reinterpret_cast` and C++23's `std::start_lifetime_as` look interchangeable. They aren't. `reinterpret_cast` is a POINTER operation. The compiler still believes whatever was at that address is whatever it was. `std::start_lifetime_as` is an OBJECT-LIFETIME operation. It actually begins the new object's life at that address. The standard guarantees one; lets you get away with the other until it doesn't. Five-line difference between UB and defined behaviour, with the obvious use cases (binary protocols, embedded MMIO, shared-memory IPC, custom allocators).

https://wrocpp.github.io/posts/fertig-reinterpret-cast/

## Hashtags
#cpp #cpp23 #reinterpretcast #memorysafety #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Fertig: this is not the cast you're looking for". Subhead: C++23 start_lifetime_as vs reinterpret_cast. Citation: wro.cpp 2026-05-21.

## Suggested post time
Thursday 2026-05-21, 10:00 CET
Reason: Mid-week morning EU audience.
