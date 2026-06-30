# One word, final, turns a virtual call into two instructions

## Body
A free performance win, visible in the assembly: mark a leaf class final and the compiler can turn a virtual call into two instructions (mov eax, 42; ret) -- no vtable, no branch. Without final, GCC keeps a runtime type check as a hedge.

We read the actual GCC 16.1 -O2 output.
https://wrocpp.github.io/posts/final-devirtualization/

## Hashtags
#cpp #performance #optimization #compilers #moderncpp

## Alt-text
A wro.cpp card showing that marking a class final reduces a virtual call to two instructions.

## Suggested post time
2026-07-12, 10:00 CET
