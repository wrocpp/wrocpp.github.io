# std::optional can finally hold a reference

## Body
std::optional<T&> has been ill-formed since C++17. Every standard library enforced it with a static_assert. The reason was not difficulty but an unresolved design question: should assignment rebind the reference, or assign through it and change the referenced object? Both are defensible, the committee could not settle it, and the feature was left out rather than shipped on a coin flip.

So we all wrote T* instead and added a comment explaining that null means absent. That works, and it loses something. A raw pointer says nothing about ownership, nothing about whether null is expected, and it composes badly with the rest of the optional-shaped API surface.

C++26 settles it. optional<T&> is legal and assignment REBINDS, matching reference_wrapper. That choice is what makes the type usable as a value: put it in a container, reassign it in a loop, return it from a function. Assign-through would have made it behave unlike every other optional in the library.

The specialization holds a pointer internally, so it costs exactly what the T* you were writing costs. What you gain is has_value(), value_or(), the monadic and_then and transform, and a type whose name states the intent.

One honest caveat: the demo compiles and runs on GCC 16.1, but libstdc++ does not yet define __cpp_lib_optional_ref, so a feature test reports it missing even where it works. Guard on compiler version for now.

https://wrocpp.github.io/posts/optional-ref/

How many T* parameters in your code really mean "maybe, and I do not own it"?

## Hashtags
#cpp #cplusplus #cpp26 #stdlib #programming #softwareengineering

## Alt-text
A cream wro.cpp social card reading "std::optional can hold a reference now", about C++26 optional of a reference.

## Suggested post time
Friday 2026-08-28, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
