# Profiles now run on Compiler Explorer: what P4415R0 reports and what I ran on both builds

## Body
C++ profiles now have two implementations, a Clang fork and a GCC fork, both on Compiler Explorer. I ran examples: with the invalidation profile enforced, GCC rejects a vector pointer used after push_back and Clang compiles it, because Clang does not know that profile.

https://wrocpp.github.io/posts/profiles-p4415-implementation-status/

## Hashtags
#cpp #cpp29 #safety #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "C++ profiles now run on two compilers" with a subtitle saying the GCC build rejects a vector use after push_back and the Clang build compiles it. Citation footer: wro.cpp, 2026-10-31.

## Suggested post time
Saturday 2026-10-31, 08:00 UTC
Reason: the first slot of the day, the follow-up announced in the mailing digest of 28 October.
