# std::rotate: how libstdc++ and libc++ actually differ

## Body
Raymond Chen wrote a three-part series on The Old New Thing (June 2-4) that exposed a surprising fact: std::rotate is implemented with completely different algorithms in libstdc++ and libc++.

libstdc++ (GCC) uses a unidirectional swap loop: n-1 swaps, good locality, friendly to the prefetcher.

libc++ (Clang) uses cycle decomposition: ~n/2 swaps (the minimum), but terrible locality -- each cycle jumps by a stride that wrecks the cache on large ranges.

The implication: the same call on the same input runs at measurably different speeds on the same machine, just by swapping compiler. For ranges under L2 with expensive moves, libc++ wins. For large ranges of cheap types, libstdc++ wins.

If std::rotate is in your hot path, benchmark on the stdlib you actually link against, or write the cycle-decomposition version explicitly for portability.

https://wrocpp.github.io/posts/std-rotate-shootout/

## Hashtags
#cpp #stdlib #libcxx #libstdcxx #algorithm #performance #moderncpp #wrocpp

## Alt-text
Editorial card: "std::rotate: libstdc++ and libc++ disagree". Algorithm comparison: n-1 swaps with locality vs ~n/2 swaps with cycle decomposition.

## Suggested post time
Thursday 2026-06-18, 10:00 CET
