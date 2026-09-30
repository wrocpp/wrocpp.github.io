# When two enumerators share a value, the value carries both names

## Body
With enum Color { red = 1, green = 1 }, enum_to_string(Color::green) returns "red". A reader pointed this out, and he is right: once green is stored in a variable, it is the same value as red.

C++26 reflection can list both names, refuse the enum at compile time with a readable error, prefer the canonical spelling through an annotation, or keep the exact name when you reflect the enumerator itself.

The names come back as string_views over static storage, so looking one up allocates nothing.

https://wrocpp.github.io/posts/enum-aliases/

## Hashtags
#cpp #cpp26 #reflection #moderncpp #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "red = 1, green = 1. Ask for green, get red." with a subtitle saying that once the value is in a variable both names are the same value, and that C++26 reflection can list them, reject them, or mark one as the alias. Citation footer: wro.cpp, 2026-10-01.

## Suggested post time
Thursday 2026-10-01, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the flagship at 08:00 UTC.
