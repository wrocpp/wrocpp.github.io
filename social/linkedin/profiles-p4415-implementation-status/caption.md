# Profiles now run on Compiler Explorer: what P4415R0 reports and what I ran on both builds

## Body
P4415R0, in the pre-Búzios mailing, reports that C++ profiles have two independent implementations: a Clang fork with the framework and most of the initialization profile, and a GCC fork that adds a first invalidation profile. Both run on Compiler Explorer, so I ran examples on them.

With the invalidation profile enforced, the GCC build rejected an unmarked owning factory, a leaked owner, a vector pointer used after push_back and a returned local address. The Clang build compiled the same file, because it does not know that profile and enforcing an unknown profile enforces nothing. The paper asks the framework to require at least a diagnostic for that case.

The initialization profile works on both builds. The post has the code, both Compiler Explorer links, and a list of what I did not check, including the paper's nineteen adversarial cases.

https://wrocpp.github.io/posts/profiles-p4415-implementation-status/

## Hashtags
#cpp #cpp26 #cpp29 #profiles #safety #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "C++ profiles now run on two compilers" with a subtitle saying the GCC build rejects a vector use after push_back and the Clang build compiles it. Citation footer: wro.cpp, 2026-10-31.

## Suggested post time
Saturday 2026-10-31, 08:00 UTC
Reason: the first slot of the day, the follow-up announced in the mailing digest of 28 October.
