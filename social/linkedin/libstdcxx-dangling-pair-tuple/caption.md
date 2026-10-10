# libstdc++ on GCC trunk rejects a pair that binds a temporary

## Body
A std::pair or std::tuple that binds a reference to a temporary no longer compiles on GCC trunk, in any language mode. GCC 16.2 rejects it from C++20 on and accepts it in C++17 and lower.

The change is libstdc++ commit 98847dc (PR108822), pushed on 28 September 2026. It removes the _GLIBCXX_DEBUG condition from the check. On trunk of 10 October, C++17 gives "static assertion failed: std::pair constructor creates a dangling reference".

The post also covers two libstdc++ security fixes from the same weeks. The fix for CVE-2026-102010 (a use-after-free in the pb_ds binary heap erase_if, CVSS 3.1 base score 7.0) is on the GCC 14, 15 and 16 release branches, but GCC 16.2 does not have it. The std::bitset wide-stream fix (PR124370) is on trunk only. Compiler Explorer runs show GCC 16.2 and trunk side by side, with AddressSanitizer reports for both bugs on 16.2.

What I did not test: clang, MSVC, GCC 16.3 and other optimization levels.

https://wrocpp.github.io/posts/libstdcxx-dangling-pair-tuple/

## Hashtags
#cpp #cplusplus #gcc #libstdcpp #security

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "GCC trunk rejects a pair that dangles, even in C++17" with a subtitle saying GCC 16.2 accepts it before C++20 and that two libstdc++ security fixes landed in the same weeks. Citation footer: wro.cpp, 2026-10-17.

## Suggested post time
Saturday 2026-10-17, 18:00 CEST (16:00 UTC)
Reason: the planned second-post slot for that day, after the evergreen post at 08:00 UTC.
