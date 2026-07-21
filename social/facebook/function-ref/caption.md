# std::function_ref borrows a callable instead of owning it

## Body
For years the default way to take a callback in C++ was std::function, and it was usually the wrong default. std::function owns its callable, so passing a lambda copies it, and a big closure allocates. When you only call the thing and return, you paid for ownership you never used.

C++26 adds std::function_ref: a non-owning reference to a callable. No copy, no allocation. It is to std::function what string_view is to string. Use it when you call the callable now and do not keep it. Use std::function when you must store it for later. Like string_view, it does not extend a lifetime, so do not store one that points at a temporary.

Full demo: https://wrocpp.github.io/posts/function-ref/

## Hashtags
#cpp #cplusplus #cpp26 #programming #softwareengineering

## Alt-text
A cream wro.cpp social card reading "The callback type that copies nothing", about C++26 std::function_ref.

## Suggested post time
Tuesday 2026-08-04, 10:00 CET
Reason: Tuesday mid-morning CET for the EU audience.
