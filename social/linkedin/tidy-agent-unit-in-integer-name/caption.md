# A TTL of 30 seconds became 30 milliseconds, and a name check flags both fields

## Body
Episode 2 of a series on clang-tidy checks for the mistakes AI coding agents keep making.

A config struct with std::int64_t ttl_sec and std::int64_t timeoutMs accepts the same number in both. Storing 30 in each compiles without a warning, and the program prints timeoutMs = 30 where 30000 was meant. With std::chrono::seconds and std::chrono::milliseconds the same assignment converts exactly, and the reverse does not compile.

The check, wrocpp-unit-in-integer-name, is a query check. It flags integer and floating variables and fields whose name ends in a unit suffix such as Ms or _sec. It reported 2 of 2 fields in the example on clang-tidy trunk (LLVM 24.0.0git) on Compiler Explorer, and none on the chrono version.

What it misses: a unit in a comment, a unit in a type alias, and suffixes not in its list, such as Milliseconds and Minutes. In a second file it reported 3 of 9 members. On cloudevents-sdk-cpp it also flagged constants like max_string_bytes, where a byte count is correct. I did not measure how often an agent breaks the equivalent rule in prose, so the post shows what the check finds and not that it beats the rule.

https://wrocpp.github.io/posts/tidy-agent-unit-in-integer-name/

## Hashtags
#cpp #clangtidy #aicoding #chrono #units #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "30 seconds became 30 milliseconds" with a subtitle about a clang-tidy query check that flags 2 of 2 unit-suffixed integer fields and cannot see a unit in a comment. Citation footer: wro.cpp, 2026-12-02.

## Suggested post time
Wednesday 2026-12-02, 08:00 UTC
Reason: the morning slot on the publication day; episode 2 of the tidy-agent series, which runs 1 to 9 December.
