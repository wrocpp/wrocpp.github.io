# Clang 23.1 -Wlifetime-safety warns on 6 of 7 dangling cases, GCC 16.2 on 1

## Body
I compiled seven small programs that dangle with Clang 23.1 and GCC 16.2.

With -Wlifetime-safety, Clang warned on six. GCC 16.2 with -Wall -Wextra -Wdangling-pointer=2 -Wdangling-reference gave one correct report, from inside a standard header. Clang already warned on three of the six without the flag. The flag adds an escaping lambda capture, a reference across push_back and a view field set from a parameter. It also flagged one correct program.

https://wrocpp.github.io/posts/clang-lifetime-safety-warnings/

## Hashtags
#cpp #clang #gcc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Clang 23.1 warns on 6 of 7 dangling cases" with a subtitle about -Wlifetime-safety and GCC 16.2. Citation footer: wro.cpp, 2026-11-23.

## Suggested post time
Monday 2026-11-23, 08:00 UTC
Reason: the morning slot on the publication day.
