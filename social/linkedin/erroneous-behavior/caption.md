# C++26 ends a 40-year footgun: uninitialized reads

## Body
`int x;` then reading x has been undefined behavior in C++ for four decades -- not "you get a random number", but "the compiler may assume this never happens" and optimize accordingly (deleted branches, time-travel miscompiles, security bugs).

C++26 changes the rule. Under P2795, reading an uninitialized variable is now ERRONEOUS behavior: a new category between fine and undefined.

Still a bug, still diagnosed -- but with defined bounds. The read yields a fixed erroneous value (GCC uses 0), not indeterminate garbage. The optimizer may not time-travel on it. It is not exploitable, and sanitizers can trap it.

The demo makes it concrete: it poisons a stack frame with 0xDEADBEEF, then reads an uninitialized int. Built as C++23 it prints leftover garbage (and it was UB). Built as C++26 -- same source -- it prints a defined 0, every run. GCC still warns either way. Runs live on Compiler Explorer.

And when you genuinely want an uninitialized buffer, C++26 keeps the door open: declare it [[indeterminate]] -- now a deliberate, greppable annotation instead of an accident.

The quiet kind of feature that retires a whole bug class without breaking one correct program.

Demo + details: https://wrocpp.github.io/posts/erroneous-behavior/ -- how many uninitialized-read bugs has this class cost you?

## Hashtags
#cpp #cplusplus #cpp26 #safety #undefinedbehavior #memorysafety #moderncpp

## Alt-text
A cream wro.cpp-branded social card titled "C++26 ends a 40-year footgun" with a sub-claim that reading an uninitialized variable is now erroneous behavior: defined, diagnosable, and not exploitable.

## Suggested post time
Sunday 2026-07-05, 14:00 CET
Reason: same-day publish; early-afternoon CET for weekend reach.
