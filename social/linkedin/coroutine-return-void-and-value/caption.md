# GCC trunk accepts a coroutine promise with return_value and return_void

## Body
GCC trunk now accepts a coroutine promise type that declares both return_value and return_void, so one coroutine can use co_return; and co_return 42; in the same body. GCC 16.2 stops with the error "the coroutine promise type declares both 'return_value' and 'return_void'".

The change is Jakub Jelinek's commit of 2026-10-03, which implements the C++29 paper P3950R1 (Robert Leahy, dated 2026-06-11) and raises __cpp_impl_coroutine from 201902L to 202606L. The commit title says "as DR"; the paper itself does not use that label.

I ran one program on Compiler Explorer on 10 October 2026. GCC trunk 17.0.0 20261010 compiles it with -std=c++20, exits 0 and prints 202606L, 0 for the empty co_return and 42 for the valued one.

What is not tested: clang, MSVC, GCC 16.3, optimization levels and flowing off the end of a coroutine. The Bugzilla page for PR125830 was behind bot protection, so I did not read it. The post also has one paragraph on the 7 October GCC modules change for P1811.

https://wrocpp.github.io/posts/coroutine-return-void-and-value/

## Hashtags
#cpp #cplusplus #cpp29 #gcc #coroutines #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo and an AI-generated label. Headline reads "A coroutine promise may now have both return_value and return_void" with a subtitle saying GCC 16.2 rejects it and GCC trunk of 2026-10-10 compiles and runs it. Citation footer: wro.cpp, 2026-10-14.

## Suggested post time
Wednesday 2026-10-14, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
