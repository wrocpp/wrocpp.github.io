# bugprone-dangling-handle flags 7 of 13 views of a temporary, GCC 16.2 flags none

## Body
Episode 4 of a series on clang-tidy checks for AI-agent mistakes. I built 13 small programs where a string_view or a view class of my own points into a temporary string. The existing check bugprone-dangling-handle flagged 7 once my class was in its list. Clang 23.1 warned on 7 or 8, GCC 16.2 on none. Three cases escaped every tool, and a deleted rvalue overload fixes the class you own.

https://wrocpp.github.io/posts/tidy-agent-view-of-temporary/

## Hashtags
#cpp #clangtidy #stringview #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "GCC 16.2 warns on none of 13 dangling views" with a subtitle about bugprone-dangling-handle flagging 7 and Clang 23.1 warning on 7 or 8. Citation footer: wro.cpp, 2026-12-04.

## Suggested post time
Friday 2026-12-04, 08:00 UTC
Reason: the morning slot on the publication day; the nine episodes run from 1 to 9 December.
