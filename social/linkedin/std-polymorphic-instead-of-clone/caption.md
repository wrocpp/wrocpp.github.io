# std::polymorphic removes clone() and the override you can forget

## Body
Episode 4 of a series on clone() and smart pointers.

std::polymorphic<Figure> copies the object it holds with that object's dynamic type, so a class with no clone hooks copies correctly. In the example, a vector of three polymorphic figures copies to three distinct objects with the same three dynamic types, and a static_assert checks a copy in constant evaluation on GCC 16.2.

The allocation count matches the older design. Copying a row of three takes 4 allocations with polymorphic and 4 with a unique_ptr and clone(). A mixin that finds the copy by reflection, with no hooks in the classes, also takes 4, and throws if it meets a class it does not search. A variant of the same three classes, built by reflection, takes 1, and it is a closed set.

The limits: polymorphic<Square> does not convert to polymorphic<Figure>, a moved-from object is valueless, and libc++ trunk on Compiler Explorer did not define __cpp_lib_polymorphic on 2026-11-09.

My default is polymorphic for value semantics, and the clone() from episode 2 when a caller needs a unique_ptr of the derived type or the code must build on libc++.

https://wrocpp.github.io/posts/std-polymorphic-instead-of-clone/

## Hashtags
#cpp #cpp26 #polymorphic #valuesemantics #smartpointers #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Copy a polymorphic object without writing clone()" with a subtitle about std::polymorphic, 4 allocations per row copy and libc++. Citation footer: wro.cpp, 2026-12-21.

## Suggested post time
Monday 2026-12-21, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run every second day, 15 to 21 December.
