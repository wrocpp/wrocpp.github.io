# constexpr catches undefined behavior at compile time and nowhere else

## Body
A static_assert over a constexpr function turns an out-of-range index into a compile error.

We wrote six bad calls: array, vector and span indexing past the end, INT_MAX plus one, division by zero and a null dereference. GCC 16.2 and Clang 23.1 rejected all six. The error texts are in the post, including the GCC message for the index cases: call to non-constexpr function std::__glibcxx_assert_fail.

Then we called the same functions with a value built from argc. They compiled without a warning. At -O2 on Compiler Explorer the array read printed 0 in one run and 32766 in another, Clang printed 990059265, and add_one(INT_MAX) > INT_MAX printed true. At -O0 the libstdc++ assertion fired and the program exited 134.

The standard says why the library cases are different: an operation with UB in the core clauses is never a constant expression, while UB specified in the library clauses is unspecified. The post lists what we did not test, including MSVC STL.

https://wrocpp.github.io/posts/catch-undefined-behavior-with-constexpr/

First of five posts on checking UB per statement.

## Hashtags
#cpp #cpp26 #constexpr #undefinedbehavior #safety #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "The same bad index: a compile error, then exit 0" with a subtitle saying that static_assert stops the build on undefined behavior and that with a run-time index at -O2 the same call printed stale memory. Citation footer: wro.cpp, 2026-11-02.

## Suggested post time
Monday 2026-11-02, 08:00 UTC (09:00 CET)
Reason: the series opener, on its own slot between the tidy-agent days.
