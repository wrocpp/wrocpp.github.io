# You do not need the fork any more

## Body
C++26 reflection does not need the Bloomberg clang fork any more. GCC 16.1 has had it since April, behind -freflection, using the standard <meta> header.

I checked with Daniel Lemire's snippet that prints values alongside their types, which uses an expansion statement, the reflection operator and range formatting at once. It compiles and runs on released GCC.

The two implementations do print different type names for the same types, so treat display_string_of as output for humans rather than something to parse.

"It is in C++26" and "you need a research fork to try it" are different statements, and the second is what stops people looking.

Runnable: https://wrocpp.github.io/posts/reflection-on-released-gcc/

## Hashtags
#cpp #cplusplus #cpp26 #programming

## Alt-text
A wro.cpp card about C++26 reflection on released GCC.

## Suggested post time
Tuesday 2026-10-20, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
