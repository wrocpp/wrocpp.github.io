# GCC trunk accepts a coroutine promise with return_value and return_void

## Body
GCC trunk now accepts a coroutine promise that declares both return_value and return_void, implementing the C++29 paper P3950R1 (commit of 2026-10-03). GCC 16.2 rejects the same program with a hard error.

On Compiler Explorer, GCC trunk 17.0.0 20261010 compiles it, exits 0 and prints __cpp_impl_coroutine as 202606L. I did not test clang, MSVC or GCC 16.3.

https://wrocpp.github.io/posts/coroutine-return-void-and-value/

## Hashtags
#cpp #cplusplus #cpp29 #gcc #coroutines #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo and an AI-generated label. Headline reads "A coroutine promise may now have both return_value and return_void" with a subtitle saying GCC 16.2 rejects it and GCC trunk of 2026-10-10 compiles and runs it. Citation footer: wro.cpp, 2026-10-14.

## Suggested post time
Wednesday 2026-10-14, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
