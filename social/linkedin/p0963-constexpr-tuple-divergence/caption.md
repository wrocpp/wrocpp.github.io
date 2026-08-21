# Three ingredients, one compiler disagreement

## Body
C++26 lets a structured binding declaration be the condition of an if, so this works:

  if (auto [a, b] = make_result()) { ... }

GCC and clang both implement it. They disagree about one corner, and I spent a while narrowing down which one.

The failure needs three ingredients at once: the binding used as a condition, a type that decomposes through the tuple protocol rather than member by member, and evaluation in a constant expression. Remove any one and GCC is happy. Keep all three and it says:

  error: accessing '<anonymous>' outside its lifetime

clang compiles the same file and runs it.

The reduced case is about twenty lines with no library involved. I found it while checking whether the new syntax shortens the canonical CTRE example, because ctre::regex_results decomposes through the tuple protocol and CTRE matches are routinely evaluated at compile time. Nothing exotic; the ingredients assemble themselves.

Workaround if you hit it: the older spelling with an explicit condition works everywhere.

Full reduction, the four-case matrix and links for both compilers: https://wrocpp.github.io/posts/p0963-constexpr-tuple-divergence/

## Hashtags
#cpp #cplusplus #cpp26 #gcc #clang #compilers

## Alt-text
A wro.cpp card reading "Three ingredients, one compiler disagreement", about a C++26 structured binding divergence.

## Suggested post time
Friday 2026-08-21, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
