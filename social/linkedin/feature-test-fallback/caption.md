# Ship the C++20 feature and its fallback in one file

## Body
The code review that started this series ended with a portability question: std::osyncstream is C++20, but not every compiler in a shipping codebase has it. The answer is to detect the feature and fall back.

Include <version>, then #if defined(__cpp_lib_syncbuf) include <syncstream> and use osyncstream, else include <mutex> and guard the write with a static mutex. On GCC 16.1 the demo prints __cpp_lib_syncbuf = 201803 and takes the syncstream path; a compiler without it compiles the mutex branch from the same source.

Why not gate on __cplusplus greater than or equal to 202002L? Because that asks the wrong question. A compiler can be in C++20 mode and still lack a given library feature, since language and library support ship at different times. The feature-test macro answers the precise question: is this facility present? Each library feature has its own macro with a date-stamped value.

<version> makes it ergonomic: included alone it defines every library feature-test macro without pulling in the features, so you can ask whether you have <syncstream> before you include it. The system is standardized in SD-6.

Episode 6 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/feature-test-fallback/

## Hashtags
#cpp #cplusplus #cpp20 #portability #featuretestmacros #moderncpp

## Alt-text
A cream wro.cpp card reading "One header: C++20 fast path, portable fallback", on feature-test macros.

## Suggested post time
Friday 2026-10-09, 10:00 CET
Reason: morning CET; Friday series lane.
