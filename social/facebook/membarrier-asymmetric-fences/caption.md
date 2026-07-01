# The syscall behind C++ asymmetric fences

## Body
A memory fence is expensive, and some concurrent code needs one on a path that runs constantly. Asymmetric fences move that cost. The common path gets a free compiler barrier; the rare path calls Linux membarrier(), which forces every OTHER thread to run a full fence for you.

We ran the classic store-buffer test with it: 50,000 trials, zero forbidden reorderings, live on Compiler Explorer.

Ryan Chung Yi Sheng's deep-dive follows the idea from the C++ standard down into the Linux kernel -- and finds a possible crack in the standard's wording along the way.

Read it: https://wrocpp.github.io/posts/membarrier-asymmetric-fences/

## Hashtags
#cpp #cplusplus #concurrency #lockfree #linux

## Alt-text
A dark wro.cpp social card titled "The syscall behind C++ asymmetric fences" with a sub-claim about paying for a memory barrier only on the rare path via Linux membarrier().

## Suggested post time
Thursday 2026-07-16, 10:00 CET
Reason: post lands on its own pubDate; Thursday mid-morning CET catches the EU working-C++ audience.
