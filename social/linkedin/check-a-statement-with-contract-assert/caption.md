# contract_assert checks one statement, and a build flag decides what a failure does

## Body
contract_assert(i < v.size()) placed in front of v[i] is a per-statement bounds check in C++26. On GCC 16.2 the source stays the same and -fcontract-evaluation-semantic decides the outcome: ignore does nothing, observe prints a violation report and continues, enforce prints it and terminates (exit 134), quick_enforce terminates without a report.

The post measures all four, plus a replacement violation handler, and the -O0 and -O2 outcomes with the assert in front of a real out-of-range read. libstdc++'s _GLIBCXX_ASSERTIONS is a separate check: it aborts with its own assertion text and never calls the contract violation handler, even under observe.

It is a statement you write, not an operator on an expression, and C++26 has no expression form for it. Clang lists contracts as unsupported, so everything was run on GCC 16.2 only. The untested list is in the post.

https://wrocpp.github.io/posts/check-a-statement-with-contract-assert/

This is the second post in a series on checking undefined behavior one statement at a time. It started with a reader comment from Zamfir Yonchev: https://www.facebook.com/wrocpp/posts/pfbid02snUq5XLSWrz81qkiZhXVSy9b5EkuNu7QU89LEe3x7rv16hc5NNBzKkCTh2kLz6qpl?comment_id=1655384732663723

## Hashtags
#cpp #cpp26 #contracts #gcc #safety #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "One assert, four outcomes, chosen by a build flag" with a subtitle saying contract_assert on GCC 16.2 can ignore, report, terminate or terminate silently. Citation footer: wro.cpp, 2026-11-04.

## Suggested post time
Wednesday 2026-11-04, 08:00 UTC (09:00 CET)
Reason: the episode slot in the series; the user schedules it.
