# libstdc++ on GCC trunk rejects a pair that binds a temporary

## Body
On GCC trunk, a std::pair or std::tuple that binds a reference to a temporary no longer compiles in any language mode. GCC 16.2 rejects it from C++20 on only.

The post also covers two libstdc++ security fixes. The CVE-2026-102010 fix is on the GCC 14, 15 and 16 release branches, and GCC 16.2 does not have it yet. The std::bitset wide-stream fix is on trunk only.

https://wrocpp.github.io/posts/libstdcxx-dangling-pair-tuple/

## Hashtags
#cpp #gcc #libstdcpp #security

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "GCC trunk rejects a pair that dangles, even in C++17" with a subtitle saying GCC 16.2 accepts it before C++20 and that two libstdc++ security fixes landed in the same weeks. Citation footer: wro.cpp, 2026-10-17.

## Suggested post time
Saturday 2026-10-17, 18:00 CEST (16:00 UTC)
Reason: the planned second-post slot for that day, after the evergreen post at 08:00 UTC.
