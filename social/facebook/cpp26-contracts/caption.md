# C++26 contracts, and the const rule the compiler makes you learn

## Body
Contracts are one of the four headline C++26 features, and the one that got the least attention. GCC 16.1 implements them, so you can write preconditions today with -fcontracts.

The syntax attaches to the declaration: pre for what the caller must guarantee, post for what the function promises, contract_assert for a check in the body.

Two surprises. A by-value parameter named in a postcondition must be const, because the body could otherwise reassign it and the postcondition would be checking the wrong value. The compiler refuses outright rather than let that slide.

And what a violation does is not in your source: it is a compile-time choice between ignore, observe (report and continue) and enforce (report and terminate, the default). Same code, three behaviours. That is what makes contracts deployable: run observe in staging to collect real violations without downtime, then switch to enforce.

Both demos run live: https://wrocpp.github.io/posts/cpp26-contracts/

## Hashtags
#cpp #cplusplus #cpp26 #contracts #programming

## Alt-text
A cream wro.cpp social card reading "A comment cannot check itself", about C++26 contracts.

## Suggested post time
Thursday 2026-08-20, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
