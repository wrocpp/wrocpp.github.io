# std::function_ref borrows a callable instead of owning it

## Body
For years the default way to take a callback in C++ was std::function, and for years it was the wrong default. std::function owns its callable. Passing a lambda to a std::function parameter copies it, and if the closure is too big for the small-object buffer, that copy allocates. When all you do is call the thing and return, you paid for ownership you never used.

C++26 adds the type most callback parameters actually wanted: std::function_ref. It is a non-owning reference to a callable, a pointer to your callable plus a pointer to how to invoke it. No copy, no allocation, no ownership. It is to std::function what string_view is to string. The demo binds one function_ref<int(int)> to a capturing lambda and a plain function pointer, both with nothing copied.

The rule is about lifetime. Use function_ref when you call the callable now and do not keep it: predicates, visitors, comparators, for-each hooks. Use std::function when you must store it past the current stack frame. The trap is string_view's trap: a function_ref does not extend the lifetime of what it points at, so binding one to a temporary and storing it dangles.

Used as a parameter it is exactly right: https://wrocpp.github.io/posts/function-ref/

How many of your std::function parameters were really borrows?

## Hashtags
#cpp #cplusplus #cpp26 #stdlib #performance #programming

## Alt-text
A cream wro.cpp social card reading "The callback type that copies nothing", about C++26 std::function_ref as a non-owning callable reference.

## Suggested post time
Tuesday 2026-08-04, 10:00 CET
Reason: Tuesday mid-morning CET, a strong weekday engagement slot for the EU C++ audience.
