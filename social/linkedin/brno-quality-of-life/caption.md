# Five small C++29 papers you will actually use

## Body
Underneath the Brno safety headlines, WG21 cleared a stack of small papers that working programmers will feel every day. None will make a keynote. All target C++29.

P2287, "Designated-initializers for Base Classes" (Revzin), finally lets designated init reach through a base class. You name the inherited member directly, with the C++20 declaration-order rule intact.

P3091, "Better Lookups for map, unordered_map, and flat_map" (Halpern), adds get(), returning optional<mapped_type&>. No insertion, works on a const map, no end() dance. Note the name: get(), not lookup().

P3668, "Defaulting Postfix Increment and Decrement Operations," lets you =default the postfix operator so it defers to the prefix one. One line of boilerplate everyone has gotten subtly wrong, deleted.

P3125, "constexpr pointer tagging" (Dusikova), standardizes std::pointer_tag_pair, and quietly reaches for the reflection operator ^^ to ask a type how many spare bits its alignment guarantees.

P3248, "Require [u]intptr_t" (Brito Gadeschi), makes intptr_t and uintptr_t mandatory instead of optional.

https://wrocpp.github.io/posts/brno-quality-of-life/

## Hashtags
#cpp #cpp29 #wg21 #moderncpp #stl #designatedinitializers #reflection #wrocpp

## Alt-text
Editorial card with headline "Five small C++29 papers you will actually use" and subtitle "Base-class designated init, a non-inserting map get(), pointer tagging, and more."

## Suggested post time
2026-06-18, 10:00 CET
