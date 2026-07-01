# The syscall behind C++ asymmetric fences

## Body
Most lock-free tricks avoid locks. Asymmetric fences avoid something more expensive on the hot path: the memory fence itself.

The idea: split a sequentially consistent fence into a cheap common path and an expensive rare path. The common path gets a light fence -- std::atomic_signal_fence, a compiler barrier that emits zero hardware instructions. The rare path does the real work for both sides. On Linux that heavy fence is one syscall, membarrier(): it interrupts every other thread in the process and makes each run a full barrier before returning. You move the cost off the path that runs constantly and onto the one that rarely needs ordering. Folly uses exactly this in hazard pointers and RCU; C++ standardized it in P1202 and [atomics.order]/4.

We ran it: a store-buffer (Dekker) test where a==0 && b==0 is forbidden under sequential consistency. Light fence on one thread, membarrier heavy fence on the other, 50,000 trials, zero forbidden outcomes -- and it runs live on Compiler Explorer (executors are Linux).

But the reason to read Ryan Chung Yi Sheng's deep-dive is what is underneath: why the naive C++ formalization chains transitively and becomes unimplementable, the wording that fixed it, and a formal kernel-memory-model argument that the context-switch case may NOT deliver the strongly-happens-before C++ now claims. A possible latent defect, found by reading two memory models against each other.

Full spotlight + runnable demo: https://wrocpp.github.io/posts/membarrier-asymmetric-fences/

## Hashtags
#cpp #cplusplus #concurrency #lockfree #memorymodel #linux #cpp26

## Alt-text
A dark wro.cpp social card titled "The syscall behind C++ asymmetric fences" with a sub-claim about paying for a memory barrier only on the rare path via Linux membarrier().

## Suggested post time
Thursday 2026-07-16, 10:00 CET
Reason: post lands on its own pubDate; Thursday mid-morning CET catches the EU working-C++ audience.
