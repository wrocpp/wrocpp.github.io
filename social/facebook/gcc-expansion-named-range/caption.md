# Naming a constant makes GCC doubt it

## Body
An expansion statement over a compile-time range compiles on GCC 16.1 when the range is written inline, and fails when the identical expression is given a name:

  error: 'members' is not a constant

Same expression, same initializer, same constexpr. clang accepts both.

The named form is the one people write: compute the member list once, name it, use it. Splitting a long expression out of a loop header is ordinary style, and here it turns a working program into a compile error whose message sounds like your code is wrong.

If you are porting reflection code written against clang, this is the shape of breakage to expect.

Reduced case, both compilers: https://wrocpp.github.io/posts/gcc-expansion-named-range/

## Hashtags
#cpp #cplusplus #gcc #programming

## Alt-text
A wro.cpp card about a GCC expansion statement limitation.

## Suggested post time
Wednesday 2026-10-21, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
