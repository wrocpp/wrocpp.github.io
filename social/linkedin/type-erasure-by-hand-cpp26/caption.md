# Sean Parent's type erasure by hand in C++26, with a 24-byte buffer and deducing this

## Body
Episode 3 of the series on pimpl and type erasure in C++26.

A drawable value holds any shape that can draw itself, report its area and scale. The shapes are plain structs with no base class. It copies like a value. The design comes from Sean Parent's talk "Better Code: Runtime Polymorphism".

Inside: a private interface with virtual functions, a class template that implements it for each stored type, and a 24-byte buffer. On GCC 16.2 the drawable is 32 bytes. A circle fits in the buffer; a square with a vector goes to the heap. Copying a row of three shapes costs 3 allocations, and the circles cost none.

One accessor written with deducing this serves both const and non-const callers. A const drawable gets a const reference to the model, which a plain pointer member would not give.

For scale: libstdc++ 16.2 keeps 16 bytes inline in std::function and 24 in std::move_only_function and std::copyable_function.

The weak spot is repetition. Every member appears three times: in the interface, in the model and in the forwarding function. Tomorrow reflection writes two of the three.

https://wrocpp.github.io/posts/type-erasure-by-hand-cpp26/

## Hashtags
#cpp #cpp26 #typeerasure #deducingthis #valuesemantics #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Runtime polymorphism with no base class, in 32 bytes" with a subtitle about Sean Parent's concept and model, a 24-byte buffer and a deducing-this accessor. Citation footer: wro.cpp, 2027-01-15.

## Suggested post time
Friday 2027-01-15, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run daily, 13 to 16 January.
