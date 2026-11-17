# The enumerator can carry its SQL name, and the build says which one is missing

## Body
Leonardo Rossi wrote a LinkedIn post on values as template parameters. I ran two of its examples.

Their claim about the getter holds in my run. A member function pointer as a template argument reads the member with one movsd and a ret on GCC 16.2, Clang 22.1 and MSVC. The same pointer passed at run time needs an add, a test, a branch and an indirect jump on GCC and Clang.

Their chain of if constexpr that maps an enum to SQL column names works in C++17, and the static_assert in its last branch does stop the build for a new enumerator. The cost is a second list: every enumerator appears in the enum and again in the chain.

With C++26 annotations the name sits on the enumerator, so the chain goes away. A static_assert with a message then names the enumerator that has no name, or repeats one, for example "Draft::Raw has no [[=sql{...}]] annotation" on GCC 16.2. The annotation version builds on GCC 16.2 only, because the Bloomberg Clang fork lacks annotations_of_with_type.

https://wrocpp.github.io/posts/enumerator-carries-its-sql-name/

## Hashtags
#cpp #cpp26 #reflection #annotations #templates #enum #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A new enumerator breaks the build, by name" with a subtitle about the SQL name as an annotation and a static_assert that names the missing one. Citation footer: wro.cpp, 2026-12-27.

## Suggested post time
Sunday 2026-12-27, 08:00 UTC
Reason: the morning slot on the publication day; one post a day from 22 December.
