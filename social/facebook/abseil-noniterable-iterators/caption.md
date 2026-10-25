# Abseil changed what an iterator does, and nothing warns you

## Body
Abseil's August LTS has a short breaking changes list. One entry: hashtable iterators returned from insert and emplace are now non iterable, and any prior use of iteration was likely a bug.

insert returns an iterator so you can reach the element without a second lookup. That still works. But what you got was an ordinary table iterator, so incrementing it compiled and walked an arbitrary suffix of the table in an unspecified order. It had the shape of a sensible range and none of the properties of one.

The fix is two bytes of static data: a full byte followed by a sentinel, with the returned iterator pointing at that instead of into the table. Dereferencing works, incrementing lands on end().

The uneasy part is that nothing warns you. Same types, same signatures. A loop that used to run now runs zero times.

https://wrocpp.github.io/posts/abseil-noniterable-iterators/

## Hashtags
#cpp #cplusplus #abseil #containers #apidesign

## Alt-text
A wro.cpp social card reading "The loop compiles and does nothing", about Abseil making insert iterators non iterable.

## Suggested post time
Saturday 2026-11-07, 08:00 UTC
Reason: the morning slot of a day with one post, moved here from 28 October for the WG21 mailing post.
