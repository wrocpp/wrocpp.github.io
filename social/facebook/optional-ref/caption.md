# std::optional can finally hold a reference

## Body
std::optional<T&> has been ill-formed since C++17, not because it was hard but because nobody could agree what assignment should mean: rebind the reference, or assign through it? The committee could not settle it, so the feature was left out.

So we all wrote T* instead and added a comment explaining that null means absent.

C++26 settles it: optional<T&> is legal and assignment rebinds, matching reference_wrapper. That choice is what makes it usable as a value you can store, reassign, and return. Internally it holds a pointer, so it costs what your T* cost. What you gain is has_value(), value_or(), the monadic helpers, and a type that states the intent.

One caveat: it runs on GCC 16.1, but libstdc++ has not set the feature-test macro yet, so guard on compiler version for now.

https://wrocpp.github.io/posts/optional-ref/

## Hashtags
#cpp #cplusplus #cpp26 #programming #softwareengineering

## Alt-text
A cream wro.cpp social card reading "std::optional can hold a reference now", about C++26 optional of a reference.

## Suggested post time
Friday 2026-08-28, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
