# One word, final, turns a virtual call into two instructions

## Body
One keyword, measurable in the assembly.

Take a virtual call through a reference to a leaf class. Without final, GCC 16.1 at -O2 hedges: it loads the vtable, compares against the expected override, inlines on the hit, and keeps an indirect jmp as a fallback. Mark the class final and the compiler can prove the type, so the whole function folds to:

  mov eax, 42
  ret

Two instructions, no vtable, no branch. final is not just documentation that a class is a leaf -- it is information the optimizer uses to devirtualize. The win is biggest in hot loops that call virtual methods on leaf types.

Real assembly, both versions linked.
https://wrocpp.github.io/posts/final-devirtualization/

## Hashtags
#cpp #performance #optimization #moderncpp #compilers #cpp26

## Alt-text
A wro.cpp card showing that marking a class final reduces a virtual call to two instructions.

## Suggested post time
2026-07-12, 10:00 CET
