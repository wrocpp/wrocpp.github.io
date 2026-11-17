# A shared_ptr nobody shares costs 24 heap bytes where a unique_ptr costs 4

## Body
Episode 7 of a series on clang-tidy checks for mistakes that AI coding agents keep making.

A local shared_ptr that is only dereferenced shares nothing. On GCC 16.2, make_shared took one 24-byte allocation for a 4-byte object and make_unique took 4. The handle is 16 bytes against 8. I did not measure time.

The tidy-agent check needless-shared-ptr is a plugin, so it ran locally on LLVM 23.1.5. It flagged 3 of 15 shapes of a local shared_ptr and left alone the nine that share the pointer or might. The fix-it renames make_shared to make_unique on an auto variable. clang-tidy printed "applied 2 of 2 suggested fixes", which counts edits: there were 3 warnings.

It has one false positive I found. A class that calls shared_from_this() is flagged, and after the fix it throws bad_weak_ptr. It also misses w == nullptr, a pointer built with new, and allocate_shared.

https://wrocpp.github.io/posts/tidy-agent-needless-shared-ptr/

## Hashtags
#cpp #clangtidy #aicoding #smartpointers #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "make_shared took 24 bytes, make_unique 4" with a subtitle about a local shared_ptr that is only dereferenced and a check that rewrites it. Citation footer: wro.cpp, 2026-12-07.

## Suggested post time
Monday 2026-12-07, 08:00 UTC
Reason: the morning slot on the publication day; the nine episodes run from 1 to 9 December.
