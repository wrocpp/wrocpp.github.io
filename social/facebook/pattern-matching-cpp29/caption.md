# Pattern matching did not make C++26

## Body
C++26 landed reflection, contracts, std::execution and std::simd, so it is easy to assume anything long-discussed made it in. Pattern matching did not. P2688 missed the freeze and now targets C++29.

There is no compiler to try it on either. No shipping GCC or Clang exposes a flag, so unlike reflection, which runs on GCC 16.1 today, there is nothing to link to.

What it would give you: an expression that inspects structure and binds parts in one construct, with destructuring built in and exhaustiveness checked. Until then the idiom is std::visit with an overload set, which does give you the exhaustiveness check but not the destructuring.

https://wrocpp.github.io/posts/pattern-matching-cpp29/

## Hashtags
#cpp #cplusplus #cpp26 #cpp29 #programming

## Alt-text
A cream wro.cpp social card reading "Pattern matching did not ship in C++26", about P2688 slipping to C++29.

## Suggested post time
Thursday 2026-08-13, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
