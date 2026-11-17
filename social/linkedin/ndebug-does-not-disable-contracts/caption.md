# -DNDEBUG does not turn off contract_assert on GCC 16.2

## Body
On GCC 16.2, -DNDEBUG deletes the assert macro and leaves contract_assert running. With -fcontracts and no semantic flag, a false condition terminates the program, and adding -O3 -flto changed nothing.

Only -fcontract-evaluation-semantic=ignore stopped the evaluation. observe reported the violation and carried on. Without -fcontracts the same file compiled and then failed to link, and I did not look into why.

I ran six flag sets on Compiler Explorer and do not know whether other GCC builds behave the same. Herik Lima's release line, which adds -DNDEBUG to the optimization and link-time flags, was the starting point.

https://wrocpp.github.io/posts/ndebug-does-not-disable-contracts/

## Hashtags
#cpp #cpp26 #contracts #gcc #releasebuilds #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "NDEBUG leaves contract checks running on GCC 16.2" with a subtitle about -fcontracts and the evaluation semantic. Citation footer: wro.cpp, 2026-11-16.

## Suggested post time
Monday 2026-11-16, 08:00 UTC
Reason: a single post that day, so the morning slot.
