# Abseil changed what an iterator does, and nothing warns you

## Body
Abseil's LTS 20260817.0 landed on 18 August with a short breaking changes list. One entry: hashtable iterators returned from insert and emplace are now non iterable, and any prior use of iteration was likely a bug.

That last clause is doing a lot of work.

insert and emplace return a pair of an iterator and a bool. The iterator points at the element, which is how you reach it without a second lookup. That is the intended use and it is unaffected.

The problem is that what you were handed was an ordinary table iterator, and ordinary table iterators increment. So walking from it compiles, and it does something. What it does is walk from wherever the key happened to hash to, through whatever the layout puts after it, to the end of storage. The order is unspecified. The starting point is a hash artefact. Insert one more element, trigger a rehash, and the set of elements visited changes completely. It has the shape of a sensible range and none of the properties of one.

The fix is smaller than you would guess. Abseil did not add a new iterator type or a flag. It added a static two byte array holding a full byte followed by a sentinel, and points the returned iterator's control pointer at that instead of into the table. Dereferencing finds the element. Incrementing steps onto the sentinel, which is what end() compares as. No new type, no extra storage per iterator, no branch on the hot path.

The part worth being uneasy about is what a caller sees. Same return type, same signature, same iterator concepts. Code that walked from an insert result compiles identically before and after. It just stops doing anything.

Abseil's position is defensible: this was almost certainly a bug wherever it appeared, so unpredictable results become no results. Both are wrong. Only one of them is quiet in a way that survives your tests.

If you use Abseil hash containers, grep for increment applied to what insert returned. There will probably be nothing, and that is the point of checking.

https://wrocpp.github.io/posts/abseil-noniterable-iterators/

When did a silent behaviour change last reach your production code?

## Hashtags
#cpp #cplusplus #abseil #containers #apidesign

## Alt-text
A wro.cpp social card reading "The loop compiles and does nothing", about Abseil making insert iterators non iterable.

## Suggested post time
Monday 2026-10-27, 09:00 CET
Reason: Weekday morning for a correctness and upgrade hazard read.
