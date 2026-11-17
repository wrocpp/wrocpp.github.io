# Two passes in one constexpr function: labels in a compile-time assembler

## Body
A forward jump needs two passes, because the label it names is not defined yet. Andrew Alekseev wrote on LinkedIn about an assembler bootstrapped from find-and-replace, where labels were the biggest problem. Their answer was to run the program twice: the first run records label addresses, the second runs for real.

In a constexpr function the two passes are two loops. Pass 1 records where each label lands. Pass 2 emits bytes with every label known. My version assembles nine real x86-64 instructions into 44 bytes, with one backward and one forward reference.

Three checks: a static_assert against bytes I derived by hand, llvm-mc from LLVM 23.1.1 reading them back as the source, and a run on native x86-64 GCC 16.2 that returns 6. It knows two registers and nine instruction forms, and every jump uses a 32-bit distance. It is a model of the label problem and not an assembler. The project has no license, so I used none of its code.

https://wrocpp.github.io/posts/constexpr-two-pass-assembler/

## Hashtags
#cpp #constexpr #assembler #x86 #compiletime #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Two passes are two loops in a constexpr function" with a subtitle about a compile-time assembler, 44 bytes of x86-64 and a program that returns 6. Citation footer: wro.cpp, 2026-12-16.

## Suggested post time
Wednesday 2026-12-16, 08:00 UTC
Reason: the morning slot on publication day.
