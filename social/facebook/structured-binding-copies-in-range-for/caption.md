# A by-value structured binding copies the element but not the iterator

## Body
for (auto [id, payload] : registry) copies every element of a std::map, as Adam Bienkunski showed, and const auto& removes the copy. But the copy does not protect the loop: if the body erases the current element, the iterator is still invalid. Copying the keys first, a snapshot, a deferred queue and erase_if stayed defined in every run.

https://wrocpp.github.io/posts/structured-binding-copies-in-range-for/

## Hashtags
#cpp #moderncpp #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A copy does not protect the iterator" with a subtitle about auto [id, payload] and erasing the current element. Citation footer: wro.cpp, 2026-12-10.

## Suggested post time
Thursday 2026-12-10, 16:00 UTC
Reason: the second slot of the day.
