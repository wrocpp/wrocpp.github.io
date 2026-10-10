# simdjson 5.0 reads struct fields in any key order

## Body
The simdjson 5.0.0 release notes (28 Sep 2026) call static reflection an officially supported feature, and reflective reads of a struct now use key selectors by default.

On Compiler Explorer, GCC 16.2 and simdjson 5.0.2 read a struct from JSON with shuffled keys, and the program exits with 0. The notes' 1.8x speedup measures parsing escaped Unicode, not reflection.

I did not test clang-p2996, other simdjson versions or performance.

https://wrocpp.github.io/posts/simdjson-5-reflection-supported/

## Hashtags
#cpp #cplusplus #cpp26 #simdjson #json #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo and an AI-generated label. Headline reads "simdjson 5.0 reads struct fields in any key order" with a subtitle about reflection being officially supported and a GCC 16.2 run on Compiler Explorer. Citation footer: wro.cpp, 2026-10-18.

## Suggested post time
Sunday 2026-10-18, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day, after the evergreen post at 08:00 UTC.
