# The magic-numbers check reports 103 bare numbers in a test suite, and 19 deserve a name

## Body
Episode 5 of the tidy-agent series on clang-tidy checks for the mistakes AI coding agents keep making.

The wrocpp-magic-numbers-in-tests check reports a bare integer in a comparison under test/. It is a query check, so it runs on Compiler Explorer. I ran it on the 43 test files of cloudevents-sdk-cpp at commit a414e8d. It printed 369 warning lines, but they collapse to 103 unique locations, because one helper header repeats its 14 hits in 20 test files.

I read each of the 103 lines. 19 are unnamed thresholds or domain constants, such as a limit of 64 or UTF-8 range bounds. 35 are sizes, counts or indices, 26 are fixture values, 14 pin a named constant and 9 are loop bounds. That is one reader's judgement, and the post lists the categories.

Two more limits. The query matches every comparison in a test file, not only assertions as the spec says. And it cannot see floating literals. The five public commits behind the check all name numbers in production code, not in tests, so the test case I measured directly.

https://wrocpp.github.io/posts/tidy-agent-magic-numbers-in-tests/

## Hashtags
#cpp #clangtidy #aiagents #tidyagent #testing #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "103 hits in one test suite, 19 worth a name" with a subtitle about a query check for bare numbers run on the 43 test files of cloudevents-sdk-cpp. Citation footer: wro.cpp, 2026-12-05.

## Suggested post time
Saturday 2026-12-05, 08:00 UTC
Reason: the morning slot on the publication day; episode 5 of 9 in the tidy-agent series.
