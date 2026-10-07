# Which checking tool catches which undefined behavior

## Body
Seven undefined statements, seven checking mechanisms, one table, all run on GCC 16.2. constexpr stops every case at compile time, and at run time each tool covers a different subset. The uninitialised read got no diagnostic from any of them.

The post shows the exact messages, where aarch64 differed, and what was not tested.

https://wrocpp.github.io/posts/match-each-ub-case-to-a-checking-tool/

## Hashtags
#cpp #cpp26 #undefinedbehavior #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Six tools, seven UB cases, none covers all at run time" with a subtitle listing index, overflow, division by zero, null and uninitialised read, each run on GCC 16.2. Citation footer: wro.cpp, 2026-11-08.

## Suggested post time
Sunday 2026-11-08, 08:00 UTC (09:00 CET)
Reason: one short post for the day, in the ub-checks-per-statement series.
