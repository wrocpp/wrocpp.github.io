# C++26 makes an uninitialized read a defined bug

## Body
Declare int x, read it before you assign to it, and for forty years the C++ standard said your whole program was undefined. Not "x holds some leftover value," but "the compiler may assume this never happens." Compilers act on that: they delete the dependent branch and propagate the impossibility backward, so a forgotten initialization becomes a miscompile or a security bug.

C++26 narrows it. Under P2795 an uninitialized read is erroneous behavior: a bug the compiler still diagnoses, but with defined limits. The value is a fixed one the implementation picks, not an indeterminate one the optimizer can reason away. The compiler may not delete the surrounding code on the assumption the read never runs, and a sanitizer can trap it.

The demo fills a stack frame with 0xDEADBEEF, then reads an uninitialized int. As C++23 it prints leftover garbage. As C++26 the same source prints a defined 0, on every run and every optimization level, because GCC initializes the variable to a fixed value. Both standards still warn with -Wuninitialized.

When you actually want an uninitialized buffer, mark it [[indeterminate]] and you get the old behavior back as an annotation you can grep for.

https://wrocpp.github.io/posts/erroneous-behavior/

## Hashtags
#cpp #cplusplus #cpp26 #safety #undefinedbehavior #memorysafety #moderncpp

## Alt-text
A cream wro.cpp-branded social card titled "C++26 makes an uninitialized read a defined bug" about P2795 reclassifying uninitialized reads from undefined to erroneous behavior.

## Suggested post time
Sunday 2026-07-05, 14:00 CET
Reason: same-day publish; early-afternoon CET for weekend reach.
