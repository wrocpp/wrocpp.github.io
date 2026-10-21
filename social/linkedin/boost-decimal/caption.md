# Boost 1.91 adds the decimal type C++ does not have

## Body
Add 0.1 to a double a thousand times and the total is 99.999999999998593. Boost.Decimal, first shipped in Boost 1.91, implements the IEEE 754 decimal formats, and the same loop in a decimal32_t gives exactly 100.

Compiler Explorer carries Boost 1.91 and 1.92, so the post has a demo that runs both loops live. It also shows why integer cents do not fix rounding: 1.005 rounded to two places in a double gives 1.00.

The post covers the three conforming types, the faster decimal_fast variants, and what 1.92 added: CUDA support and a decompose function.

https://wrocpp.github.io/posts/boost-decimal/

## Hashtags
#cpp #cplusplus #boost #decimal #floatingpoint #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "A thousand times 0.1 is not 100 in a double" with a subtitle saying Boost.Decimal 1.91 gets exactly 100 and the demo runs live. Citation footer: wro.cpp, 2026-10-28.

## Suggested post time
Thursday 2026-10-29, 08:00 UTC
Reason: single post of the day.
