# bugprone-dangling-handle flags 7 of 13 views of a temporary, GCC 16.2 flags none

## Body
Episode 4 of a series on clang-tidy checks for mistakes that AI coding agents keep making.

I wrote 13 small programs that build a view from a temporary string. Each one reads freed memory under AddressSanitizer. The existing clang-tidy check bugprone-dangling-handle flagged 7 of them once I added my own view class to its HandleClasses option. Clang 23.1 warned on 7, or 8 with -Wlifetime-safety. GCC 16.2 warned on none, with -Wall -Wextra -Wdangling-pointer=2 -Wdangling-reference.

Three cases escaped every tool I ran: a view class that is not in the list, and two functions that return a view of their argument. Only the check saw a project's own view class built from a temporary. Only Clang saw a raw pointer from c_str().

For a class you own, deleting the rvalue overload turns the mistake into a compile error. I saw no false positive on 9 safe shapes, which is a small sample.

https://wrocpp.github.io/posts/tidy-agent-view-of-temporary/

## Hashtags
#cpp #clangtidy #aicoding #stringview #lifetime #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "GCC 16.2 warns on none of 13 dangling views" with a subtitle about bugprone-dangling-handle flagging 7 and Clang 23.1 warning on 7 or 8. Citation footer: wro.cpp, 2026-12-04.

## Suggested post time
Friday 2026-12-04, 08:00 UTC
Reason: the morning slot on the publication day; the nine episodes run from 1 to 9 December.
