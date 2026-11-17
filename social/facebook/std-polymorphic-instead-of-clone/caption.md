# std::polymorphic removes clone() and the override you can forget

## Body
Episode 4 of a series on clone() and smart pointers. std::polymorphic copies the dynamic type of the object it holds, so a class with no clone hooks has no override to forget. On GCC 16.2 a row of three copies with 4 allocations, the same as unique_ptr with clone(), and a reflection-built variant needs 1. It cannot convert to a base polymorphic, and libc++ trunk did not define it on 2026-11-09.

https://wrocpp.github.io/posts/std-polymorphic-instead-of-clone/

## Hashtags
#cpp #cpp26 #polymorphic #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Copy a polymorphic object without writing clone()" with a subtitle about std::polymorphic, 4 allocations per row copy and libc++. Citation footer: wro.cpp, 2026-12-21.

## Suggested post time
Monday 2026-12-21, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
