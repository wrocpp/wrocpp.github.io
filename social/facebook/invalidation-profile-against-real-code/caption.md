# What the invalidation profile says about P4418R0's own examples

## Body
The invalidation profile of P4418R0 exists only on an experimental GCC branch. I ran the paper's examples on it, and it rejects the bad ones.

A pointer to a local stored in a global, a lambda capturing a local by reference stored in a std::function, and a this capture in a detached thread all compile with no message. The returned versions are rejected.

https://wrocpp.github.io/posts/invalidation-profile-against-real-code/

## Hashtags
#cpp #wg21 #profiles #safety #dangling #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "The profile build accepts a local's address in a global" with a subtitle about the P4418R0 invalidation profile on an experimental GCC branch. Citation footer: wro.cpp, 2026-11-15.

## Suggested post time
Sunday 2026-11-15, 16:00 UTC
Reason: the second slot of the day.
