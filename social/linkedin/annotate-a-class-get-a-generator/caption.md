# Annotate a class, get a generator: what reflection can and cannot do

## Body
A reader asked whether reflection can build a co_yield version of an ordinary class if you annotate its functions or members. Half of that works.

Annotations can skip a data member, rename one, or pick the member functions that a generator runs one at a time. Breaking out after the second of three steps leaves the third uncalled. What does not work is a lazy twin of an ordinary method. A wrapper around a method that returns a vector builds 1000 elements for 3 consumed, and the same method written as a coroutine builds 7.

C++26 reflection has no code injection, so it cannot write the coroutine for you. All runs were on GCC 16.2 and trunk, and Clang trunk on Compiler Explorer has no std::meta.

https://wrocpp.github.io/posts/annotate-a-class-get-a-generator/

## Hashtags
#cpp #cpp26 #reflection #annotations #coroutines #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Reflection cannot write your coroutine" with a subtitle about the 1000 against 7 elements built. Citation footer: wro.cpp, 2026-11-29.

## Suggested post time
Sunday 2026-11-29, 08:00 UTC
Reason: the morning slot, after the template for post it builds on.
