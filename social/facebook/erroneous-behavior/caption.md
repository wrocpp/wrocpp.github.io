# C++26 ends a 40-year footgun: uninitialized reads

## Body
Reading an uninitialized variable has been undefined behavior in C++ for 40 years -- the kind optimizers exploit into real bugs. C++26 (P2795) reclassifies it as erroneous behavior: still a bug, still warned about, but defined, bounded, and not exploitable.

The demo poisons the stack, then reads an uninitialized int. As C++23 it prints garbage; as C++26, the same code prints a defined 0, every run. Live in your browser.

And [[indeterminate]] lets you opt back out when you really want an uninitialized buffer -- on purpose this time.

Read it: https://wrocpp.github.io/posts/erroneous-behavior/

## Hashtags
#cpp #cplusplus #cpp26 #safety #programming

## Alt-text
A cream wro.cpp-branded social card titled "C++26 ends a 40-year footgun" with a sub-claim that reading an uninitialized variable is now erroneous behavior: defined, diagnosable, and not exploitable.

## Suggested post time
Sunday 2026-07-05, 14:00 CET
Reason: same-day publish; early-afternoon CET for weekend reach.
