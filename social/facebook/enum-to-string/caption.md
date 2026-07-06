# Goodbye magic_enum

## Body
`magic_enum` parses `__PRETTY_FUNCTION__` to give you `enum` <-> string. Clever, but range-bound (default `[-128, 128]`), compiler-specific, and powerless against flags enums.

C++26 reflection (P2996) replaces the trick with the real thing: `enumerators_of(^^E)` returns the actual enumerator list from the compiler. The whole library (including `from_flags_string` round-trip via `std::ranges::fold_left` + monadic optional) is 30 lines.

Series post 5 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt with GCC 16.1.

https://wrocpp.github.io/posts/enum-to-string/

## Hashtags
#cpp #cpp26 #reflection #enum #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Goodbye magic_enum: enum reflection done right". Subhead: A reflection-driven enum<->string library in 30 lines, with flags round-trip via std::ranges::fold_left + monadic optional. Citation: wro.cpp 2026-05-05.

## Suggested post time
Tuesday 2026-05-05, 10:00 CET
Reason: Mid-week morning slot for EU C++ audience.
