# A by-value structured binding copies the element but not the iterator

## Body
Adam Bienkunski showed that for (auto [id, payload] : registry) copies every element of a std::map, and that const auto& removes the copy. I counted it on GCC 16.2, Clang trunk and MSVC: three copies for three elements, none with a reference.

The copy can look like protection when the loop body changes the container. It is not. It keeps payload valid, but the iterator the loop advances is still invalidated when the body erases the current element. On libstdc++ one run visited 4 of 3 elements and AddressSanitizer said nothing.

What stayed defined in every run: copying the keys first, a snapshot of the container, a deferred queue of changes, and erase_if. GCC and Clang warn about the copy only for const auto [..], and clang-tidy performance-for-range-copy catches the plain form.

https://wrocpp.github.io/posts/structured-binding-copies-in-range-for/

## Hashtags
#cpp #cpp23 #moderncpp #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A copy does not protect the iterator" with a subtitle about auto [id, payload] and erasing the current element. Citation footer: wro.cpp, 2026-12-10.

## Suggested post time
Thursday 2026-12-10, 16:00 UTC
Reason: the second slot of the day, beside the first debugger post.
