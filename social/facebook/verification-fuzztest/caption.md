# The same assertion, as a unit test and as a fuzzer

## Body
A unit test only checks the cases you thought to write down. Google FuzzTest lets you write a property instead, a statement that should hold for every input, and the same code works as a normal test and as a coverage-guided fuzzer.

I ran it against a run-length encoder with a planted bug: run lengths are written as a single character, so any run of ten or more identical bytes breaks the round trip.

The result is the interesting part. With no fuzzing flag at all, just the ordinary test run, the hand-written test passed and the property failed in about a second. You do not have to adopt fuzzing to benefit. Write the assertion as a property and the bug shows up in CI.

Real output and a runnable project: https://wrocpp.github.io/posts/verification-fuzztest/

## Hashtags
#cpp #cplusplus #fuzzing #testing #programming

## Alt-text
A cream wro.cpp social card reading "The bug surfaced before anyone ran a fuzzer", about Google FuzzTest.

## Suggested post time
Tuesday 2026-08-18, 10:00 CET
Reason: Tuesday mid-morning CET for the EU audience.
