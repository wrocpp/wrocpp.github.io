# C++29 mode is open, and the compilers already disagree

## Body
C++26 was finished in March. The next one is now something you can compile against.

LLVM 23.1.0 shipped on 25 August with std=c++2d, and GCC's development branch has it too. Neither current release accepts the flag at all.

Print __cplusplus in both trunks and you get 202700, the same placeholder from two independent implementations.

Ask them about C++26 and they split. GCC says 202603. Clang says 202400.

202603 is correct: C++26 was completed in March 2026, and the macro is year and month. Clang is still reporting the placeholder it used while the standard was in progress.

Plenty of existing code tests __cplusplus directly, so a comparison written against the ratified value takes the wrong branch on clang.

https://wrocpp.github.io/posts/cpp29-mode-is-open/

## Hashtags
#cpp #cplusplus #cpp26 #cpp29 #clang

## Alt-text
A wro.cpp social card reading "The compilers disagree about C++26", about __cplusplus reporting 202603 on GCC and 202400 on clang.

## Suggested post time
Wednesday 2026-09-02, 09:00 CET
Reason: Weekday morning for a standards and conformance read.
