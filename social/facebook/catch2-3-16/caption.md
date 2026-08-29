# Catch2 3.16 fixes a bug that shipped with the feature

## Body
Catch2 3.16.0 came out on 25 August. No new API, no language requirement change. Mostly performance work and CMake fixes.

One entry stands out. catch_discover_tests was not escaping test names, so a name containing a semicolon got split into several partial names. Semicolons are how CMake spells a list. The release notes say this bug has existed since the first version of the script.

It survived that long because it only bites people who punctuate test names, and the failure is a test that quietly does not run. A test that vanishes from the list looks exactly like a test that passed.

Elsewhere: registration went from about 1000 to about 3000 tests per second, and void returning benchmarks now get an optimizer barrier, so their numbers should be more honest and possibly worse.

https://wrocpp.github.io/posts/catch2-3-16/

## Hashtags
#cpp #cplusplus #catch2 #testing #cmake

## Alt-text
A wro.cpp social card reading "A bug that shipped with the feature", about Catch2 fixing semicolon handling in catch_discover_tests.

## Suggested post time
Saturday 2026-10-31, 10:00 CET
Reason: Weekend mid morning for a tooling read.
