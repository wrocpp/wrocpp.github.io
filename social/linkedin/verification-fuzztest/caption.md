# The same assertion, as a unit test and as a fuzzer

## Body
A unit test only checks the cases you thought to write down. Fuzzing checks the ones you did not, and for most teams it stays a specialist activity: a separate target, a separate build, a job nobody owns.

Google FuzzTest collapses that. You write a property, a statement that should hold for every input, and the same code serves as a bounded randomized test in your normal suite and as a coverage-guided fuzzer when you ask for fuzzing mode.

I ran it against a run-length encoder with a planted bug: the run length is written as a single character, so any run of ten or more identical bytes does not survive the round trip. The kind of bug that passes review because the example everyone tries has short runs.

Here is the part worth dwelling on. No fuzzing flag, no fuzzing job, just the ordinary test suite:

  1 PASSED, 1 FAILED

One second of bounded random inputs, and the hand-written test passed while the property failed. You do not have to adopt fuzzing as a practice to get value. You write the assertion as a property instead of an example, and the bug shows up in CI like any other failure. FuzzTest then prints a regression test draft to paste back.

Also worth knowing: libFuzzer has been in maintenance mode since 2022, its authors moved to Centipede (now in the FuzzTest repo), and OSS-Fuzz's LLM-generated targets found CVE-2024-9143, a twenty-year-old OpenSSL bug. The limit was never compute. Nobody had written a target that reached the code.

Episode 2, with the real output and a runnable CMake project: https://wrocpp.github.io/posts/verification-fuzztest/

Have you tried property-based testing in C++?

## Hashtags
#cpp #cplusplus #fuzzing #testing #security #softwareengineering

## Alt-text
A cream wro.cpp social card reading "The bug surfaced before anyone ran a fuzzer", about Google FuzzTest property testing.

## Suggested post time
Tuesday 2026-08-18, 10:00 CET
Reason: Tuesday mid-morning CET is a strong weekday slot for the EU C++ audience.
