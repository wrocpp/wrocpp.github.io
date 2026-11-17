# The enumerator can carry its SQL name, and the build says which one is missing

## Body
Leonardo Rossi wrote a LinkedIn post on values as template parameters. I reran its getter on GCC 16.2, Clang 22.1 and MSVC, and the template version is one movsd and a ret. Their if constexpr chain from enum to SQL name works in C++17 and its static_assert catches a new enumerator. With C++26 annotations the name moves onto the enumerator, and a static_assert with a message names the one that has none. That part builds on GCC 16.2 only.

https://wrocpp.github.io/posts/enumerator-carries-its-sql-name/

## Hashtags
#cpp #cpp26 #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A new enumerator breaks the build, by name" with a subtitle about the SQL name as an annotation and a static_assert that names the missing one. Citation footer: wro.cpp, 2026-12-27.

## Suggested post time
Sunday 2026-12-27, 08:00 UTC
Reason: the morning slot on the publication day; one post a day from 22 December.
