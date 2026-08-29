# The most expensive no-op in C++

## Body
Writing ~Widget() = default looks free. It removes move construction and move assignment.

Most people know the rule abstractly. C++26 reflection lets you check it: members_of gives every member the compiler produced, is_function and is_deleted sort them, and counting turns Hinnant's table into something the program prints.

Six special members become four the moment you default the destructor. Declare a move operation instead and the copies are generated as deleted rather than absent, which at least gives a diagnostic that names them.

Approach credited to Lieven de Cock's article in the August Overload. What I added is a runnable link and all eight rows.

Try it: https://wrocpp.github.io/posts/reflect-special-members/

## Hashtags
#cpp #cplusplus #cpp26 #programming

## Alt-text
A wro.cpp card about a defaulted destructor removing move operations.

## Suggested post time
Wednesday 2026-10-28, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
