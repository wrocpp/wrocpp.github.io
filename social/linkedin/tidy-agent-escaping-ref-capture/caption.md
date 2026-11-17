# The escaping-ref-capture check flags 6 of 9 dangling lambdas and 3 of 5 safe ones

## Body
Episode 8 of a series on clang-tidy checks for mistakes that AI coding agents keep making.

I wrote 9 small cases where a lambda captures a local by reference and outlives its function. The tidy-agent plugin check wrocpp-escaping-ref-capture flagged 6: the lambda returned directly, returned as a std::function, or stored in a registry. All 9 fail under AddressSanitizer on GCC 16.2 and Clang 22.1.

Clang 23.1 warned on 1 case, or 4 with -Wlifetime-safety. Together with the check, that covers 7 of 9. Case 8 escaped every tool: a lambda first bound to an auto variable and then added to a registry. GCC 16.2 at -O2 reported 3 cases, worded as an uninitialized value.

The check also reported 3 of my 5 correct cases, including one its own spec says it must not flag. It is a plugin without a fix-it, so it ran locally on LLVM 23.1.5. The post lists what it cannot see.

https://wrocpp.github.io/posts/tidy-agent-escaping-ref-capture/

## Hashtags
#cpp #clangtidy #aicoding #lambda #lifetime #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "6 of 9 dangling lambdas flagged, and 3 of 5 safe ones" with a subtitle about the tidy-agent plugin check and Clang 23.1 warning on 1 or 4 of the 9. Citation footer: wro.cpp, 2026-12-08.

## Suggested post time
Tuesday 2026-12-08, 08:00 UTC
Reason: the morning slot on the publication day; the nine episodes run from 1 to 9 December.
