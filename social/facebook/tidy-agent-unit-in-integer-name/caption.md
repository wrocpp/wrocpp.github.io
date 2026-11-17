# A TTL of 30 seconds became 30 milliseconds, and a name check flags both fields

## Body
Episode 2 of a series on clang-tidy checks for AI-written C++. Storing 30 in both ttl_sec and timeoutMs compiles without a warning, and the timeout is 1000 times too short. A query check that flags integers with a unit in the name reported 2 of 2 fields in the example. It misses a unit in a comment or a type alias, and it flags correct byte counts.

https://wrocpp.github.io/posts/tidy-agent-unit-in-integer-name/

## Hashtags
#cpp #clangtidy #chrono #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "30 seconds became 30 milliseconds" with a subtitle about a clang-tidy query check that flags 2 of 2 unit-suffixed integer fields and cannot see a unit in a comment. Citation footer: wro.cpp, 2026-12-02.

## Suggested post time
Wednesday 2026-12-02, 08:00 UTC
Reason: the morning slot on the publication day; episode 2 of the tidy-agent series, which runs 1 to 9 December.
