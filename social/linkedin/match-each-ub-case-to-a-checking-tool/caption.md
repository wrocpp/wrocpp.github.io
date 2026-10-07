# Which checking tool catches which undefined behavior

## Body
A vector index past the end, INT_MAX + 1, an integer division by zero, a null dereference and an uninitialised read: this post runs each of them under constexpr, contract_assert, _GLIBCXX_ASSERTIONS, UBSan, ASan, -ftrapv and C++26 erroneous behavior on GCC 16.2, and puts the results in one table.

constexpr stops all of them, but only inside a constant expression. At run time each tool covers a different subset: _GLIBCXX_ASSERTIONS stops the library calls, UBSan reports overflow, division, null and the array index but was silent on the vector index, ASan stops both index cases, and -ftrapv only touches overflow. For the uninitialised read nothing printed a diagnostic, and erroneous behavior gives it the value 0.

None of the tools is an operator on a single expression, and no such operator exists in C++26. The post lists the exact messages, what differed on aarch64 (integer division by zero printed 0), and what was not tested: Clang, MSVC, other GCC versions and combined builds.

https://wrocpp.github.io/posts/match-each-ub-case-to-a-checking-tool/

This is episode 4 of a series that started from a reader question about checking undefined behavior per statement.

## Hashtags
#cpp #cpp26 #undefinedbehavior #sanitizers #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Six tools, seven UB cases, none covers all at run time" with a subtitle listing index, overflow, division by zero, null and uninitialised read, each run on GCC 16.2. Citation footer: wro.cpp, 2026-11-08.

## Suggested post time
Sunday 2026-11-08, 08:00 UTC (09:00 CET)
Reason: one short post for the day, in the ub-checks-per-statement series.
