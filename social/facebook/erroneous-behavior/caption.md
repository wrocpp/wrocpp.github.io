# C++26 makes an uninitialized read a defined bug

## Body
Read an uninitialized variable in C++ and for forty years it was undefined behavior: the compiler could assume it never happened and optimize the surrounding code away, turning a forgotten initialization into a real bug.

C++26 (P2795) makes it erroneous behavior instead. It is still a bug the compiler warns about, but the value is now defined, and the optimizer can no longer reason it away.

The demo fills the stack with 0xDEADBEEF, then reads an uninitialized int. As C++23 it prints garbage. As C++26 the same code prints a defined 0. You can also opt back out with [[indeterminate]] when you want a raw buffer on purpose.

https://wrocpp.github.io/posts/erroneous-behavior/

## Hashtags
#cpp #cplusplus #cpp26 #safety #programming

## Alt-text
A cream wro.cpp-branded social card titled "C++26 makes an uninitialized read a defined bug" about P2795 reclassifying uninitialized reads from undefined to erroneous behavior.

## Suggested post time
Sunday 2026-07-05, 14:00 CET
Reason: same-day publish; early-afternoon CET for weekend reach.
