# Reflection writes the type-erasure table, and C++26 still makes you write the member names

## Body
Episode 4, the last of the series on pimpl and type erasure in C++26.

Yesterday's drawable named each member three times. Here the interface is a plain struct with three declarations, and reflection builds the rest. It lists the member functions and builds the dispatch table with define_aggregate. Then it fills the table with thunks that call the stored type's member of the same name.

On GCC 16.2, GCC trunk and the Bloomberg Clang fork the result prints the same shapes and area as the hand-written version and is the same 32 bytes.

One thing is missing. C++26 reflection can define data members but cannot add member functions to a class. So the generated value is called as v.call<^^I::draw>(out). Code injection is a separate proposal, P3294, which the paper tracker labels for C++29.

The workaround is a struct with one forwarding line per member. That brings back d.draw(out) and is one place per member instead of three.

The constraints check the rest at compile time: a shape without scale() does not convert, and a non-const member cannot be called through a const value.

https://wrocpp.github.io/posts/type-erasure-by-reflection/

## Hashtags
#cpp #cpp26 #reflection #typeerasure #defineaggregate #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Reflection writes the table, you still write the names" with a subtitle about define_aggregate building a type-erasure table and the one forwarding line per member that C++26 still needs. Citation footer: wro.cpp, 2027-01-16.

## Suggested post time
Saturday 2027-01-16, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run daily, 13 to 16 January.
