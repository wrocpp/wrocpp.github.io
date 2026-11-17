# A shared_ptr nobody shares costs 24 heap bytes where a unique_ptr costs 4

## Body
Episode 7 of a series on clang-tidy checks for AI-agent mistakes. A local shared_ptr that is only dereferenced shares nothing, yet on GCC 16.2 make_shared took 24 bytes where make_unique took 4. The tidy-agent check flagged 3 of 15 shapes and its fix-it renames the factory on an auto variable. It has one false positive: a class that uses shared_from_this() throws after the fix.

https://wrocpp.github.io/posts/tidy-agent-needless-shared-ptr/

## Hashtags
#cpp #clangtidy #smartpointers #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "make_shared took 24 bytes, make_unique 4" with a subtitle about a local shared_ptr that is only dereferenced and a check that rewrites it. Citation footer: wro.cpp, 2026-12-07.

## Suggested post time
Monday 2026-12-07, 08:00 UTC
Reason: the morning slot on the publication day; the nine episodes run from 1 to 9 December.
