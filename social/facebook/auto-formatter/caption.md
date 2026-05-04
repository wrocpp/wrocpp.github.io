# Reflect_print: auto std::formatter for any aggregate

## Body
Rust has `#[derive(Debug)]`. C++ until 2026 had `operator<<` written by hand per type. C++26 reflection ends that: one `std::formatter` specialisation walks any aggregate at compile time and prints all fields with names. Nested aggregates print recursively. Rename a field -- print follows.

Series post 6 of 25 in the wro.cpp C++26 reflection arc. Live demo on Godbolt.

https://wrocpp.github.io/posts/auto-formatter/

## Hashtags
#cpp #cpp26 #reflection #format #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Reflect_print: auto std::formatter for any aggregate". Subhead: One header replaces every operator<< and fmt specialisation. Citation: wro.cpp 2026-05-07.

## Suggested post time
Thursday 2026-05-07, 10:00 CET
Reason: Mid-week morning slot for EU C++ audience.
