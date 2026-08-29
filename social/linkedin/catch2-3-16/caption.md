# Catch2 3.16 fixes a bug that shipped with the feature

## Body
Catch2 3.16.0 came out on 25 August, the same day as LLVM 23.1 and CMake 4.4.3. It adds no API and changes no language requirement. Most of it is performance work and CMake fixes.

One entry stands out, and not because it is dramatic. catch_discover_tests is the CMake function that enumerates your tests at build time so CTest can run them individually. Its TESTS variable was not escaping test names, so a name containing a semicolon got split into several partial names. The release notes are direct about the age of it: this bug has existed since the first version of the script.

Semicolons are how CMake spells a list. A string containing one is a list of two things unless somebody escapes it. It survived this long because it only affects people who put punctuation in test names, and the failure mode is a test that quietly does not run rather than an error. Rare trigger plus silent failure is what lets a bug reach adulthood. A test that vanishes from the list looks exactly like a test that passed.

The rest is speed. Test registration went from roughly 1000 to roughly 3000 tests per second. The string matchers were rewritten, with case sensitive matching significantly faster. Compilation improved where several templated test case macros use the same types.

One change affects measurements rather than performance. Benchmarks that return nothing now get an optimizer barrier around the call. When a benchmarked function returns a value the usual trick is to keep it alive so the optimiser cannot delete the work, but with no return value there is nothing to hold, and a compiler may merge or drop consecutive calls. The barrier limits what moves between them, so numbers from void returning benchmarks should be more honest and quite possibly worse.

If you track results over time and a void returning case suddenly reports more work after upgrading, that is the fix rather than a regression.

https://wrocpp.github.io/posts/catch2-3-16/

How would you notice a test that silently stopped being registered?

## Hashtags
#cpp #cplusplus #catch2 #testing #cmake

## Alt-text
A wro.cpp social card reading "A bug that shipped with the feature", about Catch2 fixing semicolon handling in catch_discover_tests.

## Suggested post time
Saturday 2026-10-31, 10:00 CET
Reason: Weekend mid morning for a tooling read.
