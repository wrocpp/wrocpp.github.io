# contract_assert checks one statement, and a build flag decides what a failure does

## Body
Put contract_assert(i < v.size()) in front of v[i] and C++26 gives you a bounds check on that one statement. On GCC 16.2 one flag, -fcontract-evaluation-semantic, picks what a failure does: ignore, observe (report and continue), enforce (report and terminate) or quick_enforce (terminate, no report).

libstdc++'s _GLIBCXX_ASSERTIONS is a different mechanism and does not call the contract violation handler. The post shows the measured output of each and lists what was not tested, including Clang, which has no contracts.

https://wrocpp.github.io/posts/check-a-statement-with-contract-assert/

## Hashtags
#cpp #cpp26 #contracts #gcc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "One assert, four outcomes, chosen by a build flag" with a subtitle saying contract_assert on GCC 16.2 can ignore, report, terminate or terminate silently. Citation footer: wro.cpp, 2026-11-04.

## Suggested post time
Wednesday 2026-11-04, 08:00 UTC (09:00 CET)
Reason: the episode slot in the series; the user schedules it.
