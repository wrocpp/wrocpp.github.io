# Pattern matching did not make C++26

## Body
C++26 is a large release. Reflection, contracts, std::execution, std::simd, hardened library modes: enough landed that it is easy to assume anything long-discussed made it in. Pattern matching is the one people most often get wrong.

It did not ship in C++26. P2688 missed the feature freeze and the work now targets C++29.

There is no compiler you can try it on either. No shipping GCC or Clang exposes a flag for it, and it is not hiding behind an experimental switch, so unlike reflection, which you can run on GCC 16.1 today, there is nothing to link to. Worth saying plainly, because "coming in C++26" has been repeated in enough talks and comment threads to become received wisdom.

What the proposal would give you is an expression that inspects a value's structure and binds parts of it in one construct. Three things make that better than a chain of if constexpr or a visitor: it is an expression so it produces a value, destructuring is built in, and exhaustiveness can be checked so adding a new alternative makes the compiler point at the matches that no longer cover everything.

Today the idiom remains std::visit with an overload set, which C++23's deducing-this made less awkward to build. That gives you the exhaustiveness check, since visit fails to compile when a handler is missing. What it does not give you is destructuring.

C++29 is the target. Write the visitor: https://wrocpp.github.io/posts/pattern-matching-cpp29/

## Hashtags
#cpp #cplusplus #cpp26 #cpp29 #wg21 #programming

## Alt-text
A cream wro.cpp social card reading "Pattern matching did not ship in C++26", about P2688 slipping to C++29.

## Suggested post time
Thursday 2026-08-13, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
