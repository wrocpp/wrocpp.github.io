# When two enumerators share a value, the value carries both names

## Body
Boguslaw Branicki left a comment on a reflection-based enum_to_string. With enum Color { red = 1, green = 1 }, enum_to_string(Color::green) returns "red". He is right. Color::green and Color::red are the same value, so a function that takes a Color receives both names or neither.

C++26 reflection gives four answers. List every name for the value: names_of(green) returns red and green. Reject the enum at compile time: a consteval check throws std::meta::exception, and GCC 16.2 prints "Color::green duplicates Color::red (= 1)". Mark the intended alias with an annotation, which P3394 allows on enumerators, so to_string returns the canonical spelling. Or keep the reflection itself: name_of<^^green>() returns green, because only a reflection still knows which enumerator you wrote.

His second point was about returning std::string. identifier_of returns a string_view over null-terminated characters with static storage duration, so the name never allocates. The demo counts it: 0 allocations for the view, 1 for a std::string copy of a 19 character name.

The post also compares magic_enum, Boost.Describe and Better Enums. They return the first name, the last name, and an unspecified one.

https://wrocpp.github.io/posts/enum-aliases/

Do your enums have aliases on purpose, or would you rather the compiler refused them?

## Hashtags
#cpp #cpp26 #reflection #enums #moderncpp #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "red = 1, green = 1. Ask for green, get red." with a subtitle saying that once the value is in a variable both names are the same value, and that C++26 reflection can list them, reject them, or mark one as the alias. Citation footer: wro.cpp, 2026-10-01.

## Suggested post time
Thursday 2026-10-01, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the cross-language flagship at 08:00 UTC, so the page is live and the two posts do not compete.
