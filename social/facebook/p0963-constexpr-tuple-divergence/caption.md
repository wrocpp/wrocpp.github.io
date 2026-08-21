# Three ingredients, one compiler disagreement

## Body
C++26 lets a structured binding be the condition of an if. GCC and clang both implement it, and disagree about one corner.

It needs three things together: the binding as a condition, a type that decomposes through the tuple protocol, and constant evaluation. Drop any one and GCC accepts it. Keep all three and it reports accessing an anonymous object outside its lifetime, while clang compiles and runs the same file.

The reduced case is twenty lines with no library involved.

Reduction and links for both compilers: https://wrocpp.github.io/posts/p0963-constexpr-tuple-divergence/

## Hashtags
#cpp #cplusplus #cpp26 #programming

## Alt-text
A wro.cpp card about a C++26 structured binding divergence between GCC and clang.

## Suggested post time
Friday 2026-08-21, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
