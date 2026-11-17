# clang-tidy flags four objects built in steps, and its fix mode rewrites only the struct

## Body
Episode 6 of the tidy-agent series on clang-tidy checks for the mistakes AI coding agents keep making.

An agent writes a struct and then one assignment per member, or a vector and then a run of push_back calls. The wrocpp-default-then-assign check reports that shape. On a 93-line example it reports four sites. In fix mode it rewrites the one that is an aggregate into a designated initializer, and the fixed file prints the same output.

The limits are in the post. There is no fix for the vector, for a class with a constructor, or for a member assigned twice. The fix writes members in declaration order, so given p.y = next(); p.x = next(); it swaps the two values (the probe printed 2 1 before and 1 2 after). The check misses the pattern when another statement sits between the assignments.

GCC 16.2 rejects a member named twice in a designated initializer. Clang 22.1 only warns. The assignment form gives neither. The check is a plugin, so I ran it locally with clang-tidy 23.1.5, and I ran it on the public cloudevents-sdk-cpp history too: 4 sites before the commit that rewrote them, 2 left at head.

https://wrocpp.github.io/posts/tidy-agent-default-then-assign/

## Hashtags
#cpp #clangtidy #aiagents #tidyagent #designatedinitializers #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Four objects built in steps, and one fix-it" with a subtitle about the tidy-agent check, fix mode on a struct and a fix that swaps values. Citation footer: wro.cpp, 2026-12-06.

## Suggested post time
Sunday 2026-12-06, 08:00 UTC
Reason: the morning slot on the publication day; episode 6 of 9 in the tidy-agent series.
