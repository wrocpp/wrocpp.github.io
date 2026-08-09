# C++26 contracts, and the const rule the compiler makes you learn

## Body
C++26 shipped four headline features: reflection, std::execution, std::simd and contracts. Contracts got the least attention, partly because the design was contested right up to the vote and partly because until recently there was nothing to try. GCC 16.1 implements P2900, so you can write preconditions today.

The syntax attaches to the declaration: pre for what the caller must guarantee, post for what the function promises (with r: naming the result), and contract_assert for a check inside the body. No header needed, though GCC still wants -fcontracts.

Two things surprise you on first contact.

First, a by-value parameter named in a postcondition must be const, and the compiler says so outright. The reason is sound: a postcondition runs after the body, and the body can reassign a by-value parameter, so r == a would be comparing against whatever a holds at the end rather than what the caller passed. Instead of letting you write a postcondition that quietly means something else, the standard makes you prove the parameter did not change.

Second, what a violation does is not in your source at all. It is an evaluation semantic chosen at compile time: ignore does not check, observe reports and continues, enforce reports and terminates (the default). Same code, three behaviours.

That flag is what makes contracts deployable. Build with observe in staging, collect violations from real traffic without taking the service down, then switch to enforce once the reports go quiet.

Both demos run live: https://wrocpp.github.io/posts/cpp26-contracts/

Which functions in your code have a "must be positive" comment that nothing checks?

## Hashtags
#cpp #cplusplus #cpp26 #contracts #correctness #programming

## Alt-text
A cream wro.cpp social card reading "A comment cannot check itself", about C++26 contracts on GCC 16.1.

## Suggested post time
Thursday 2026-08-20, 10:00 CET
Reason: mid-morning CET on the post's pubDate for the EU audience.
