# What the invalidation profile says about P4418R0's own examples

## Body
The invalidation profile of P4418R0 exists only on an experimental GCC branch, listed on Compiler Explorer as gcontracts-p4324-trunk. I ran the paper's examples on it on 2 November 2026. It rejects the bad ones, with messages that match the paper.

Then I tried escapes the paper's rules appear to cover. A pointer to a local stored in a global, a reference-capturing lambda stored in a std::function, and a this capture handed to a detached thread all compile with exit code 0 and no message. The returned versions of the same cases are rejected.

Section 6 of the paper gives the first case as an error. It shows no example of the other stored versions, so I cannot say it means to reject them.

https://wrocpp.github.io/posts/invalidation-profile-against-real-code/

## Hashtags
#cpp #wg21 #profiles #safety #dangling #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "The profile build accepts a local's address in a global" with a subtitle about the P4418R0 invalidation profile on an experimental GCC branch. Citation footer: wro.cpp, 2026-11-15.

## Suggested post time
Sunday 2026-11-15, 16:00 UTC
Reason: the second slot of the day.
