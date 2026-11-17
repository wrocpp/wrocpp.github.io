# clang-tidy flags four objects built in steps, and its fix mode rewrites only the struct

## Body
Episode 6 of the tidy-agent series. An agent writes a struct and then one assignment per member, and the wrocpp-default-then-assign check reports it. On a 93-line example it reports four sites, and fix mode rewrites the one aggregate into a designated initializer. It has no fix for a vector or a class with a constructor, and its fix swaps two values when the right-hand sides have side effects. The check is a plugin, so I ran it locally with clang-tidy 23.1.5.

https://wrocpp.github.io/posts/tidy-agent-default-then-assign/

## Hashtags
#cpp #clangtidy #aiagents #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Four objects built in steps, and one fix-it" with a subtitle about the tidy-agent check, fix mode on a struct and a fix that swaps values. Citation footer: wro.cpp, 2026-12-06.

## Suggested post time
Sunday 2026-12-06, 08:00 UTC
Reason: the morning slot on the publication day; episode 6 of 9 in the tidy-agent series.
