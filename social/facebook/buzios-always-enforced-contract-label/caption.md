# A contract assertion labelled enforced still terminates under ignore

## Body
P4451R2, adopted at the Buzios meeting, adds a label that makes one contract assertion terminate whatever the build asks for. On GCC and Clang branch builds on Compiler Explorer, a function with 3 labelled and 3 unlabelled assertions ran 6 predicates under observe and 3 under ignore, and a violated label ended the program in 12 of 12 runs. GCC 16.2 rejects the syntax, and the EDG branch enforced nothing. I take no side in the contracts dispute. The post has the rules by paper section and every run.

https://wrocpp.github.io/posts/buzios-always-enforced-contract-label/

## Hashtags
#cpp #cpp26 #contracts #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A contract check the build cannot ignore" with a subtitle about P4451R2, 3 of 6 predicates under ignore and 12 of 12 terminating runs. Citation footer: wro.cpp, 2026-11-23.

## Suggested post time
Monday 2026-11-23, 16:00 UTC
Reason: the second post of the day; the four Buzios posts run at 16:00 UTC from 22 November.
