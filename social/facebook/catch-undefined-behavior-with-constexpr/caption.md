# constexpr catches undefined behavior at compile time and nowhere else

## Body
Six bad calls inside a static_assert: an index past the end of an array, a vector and a span, INT_MAX plus one, a division by zero and a null dereference. GCC 16.2 and Clang 23.1 stopped the build on every one.

The same functions called with a run-time value compiled cleanly. At -O2 the out-of-range read printed 0 in one run and 32766 in the next.

The post has the exact error texts, the [expr.const] wording, and a list of what we did not test.

https://wrocpp.github.io/posts/catch-undefined-behavior-with-constexpr/

## Hashtags
#cpp #cpp26 #constexpr #safety #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "The same bad index: a compile error, then exit 0" with a subtitle saying that static_assert stops the build on undefined behavior and that with a run-time index at -O2 the same call printed stale memory. Citation footer: wro.cpp, 2026-11-02.

## Suggested post time
Monday 2026-11-02, 18:00 UTC (19:00 CET)
Reason: the evening slot, after the LinkedIn post.
