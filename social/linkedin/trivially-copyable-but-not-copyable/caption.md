# Trivially copyable, and not copyable

## Body
Here is a type. On a conforming compiler, all three of these hold:

  static_assert(std::is_trivially_copyable_v<Nutshell>);
  static_assert(!std::is_copy_constructible_v<Nutshell>);
  static_assert(!std::is_copy_assignable_v<Nutshell>);

Trivially copyable, and you cannot copy it.

The type comes from Arthur O'Dwyer's P3279R0. It holds a member with a user-provided copy constructor, and declares its own move operations as defaulted. That last part is the mechanism, and it is easy to miss: declaring the move operations suppresses the copy operations, so the type has no eligible copy constructor and no eligible copy assignment at all. The standard asks whether every eligible copy or move operation is trivial. Delete the copies and only the trivial moves are left, so the condition holds by having nothing left to fail.

The paper reports that EDG and MSVC say true while clang and GCC say false, and states plainly that EDG and MSVC are correct according to the standard. That was May 2024. I checked, and two years on it is unchanged: MSVC 19.51 true, GCC 16.1 and clang 22.1 false.

One thing worth correcting, because the case travels in a shortened form. It is often described as "a trivially copyable type with a non-trivially-copyable member", which makes it sound like any aggregate would do. It would not. A plain aggregate of such members is false everywhere, MSVC included. The defaulted move declarations do all the work.

The practical takeaway is smaller than the committee argument. is_trivially_copyable_v<T> is not a licence to memcpy a T unless you have also checked that copying is something T supports. Pair it with is_copy_constructible_v and you will not care how this is resolved.

Three compilers, one file: https://wrocpp.github.io/posts/trivially-copyable-but-not-copyable/

## Hashtags
#cpp #cplusplus #typetraits #msvc #conformance

## Alt-text
A wro.cpp card reading "Trivially copyable, and not copyable", about a type-trait divergence between compilers.

## Suggested post time
Thursday 2026-10-22, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
