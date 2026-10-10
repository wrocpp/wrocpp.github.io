# simdjson 5.0 reads a struct from JSON keys in any order

## Body
The simdjson 5.0.0 release notes (28 Sep 2026) call static reflection an officially supported feature. When the compiler has reflection enabled, such as GCC 16 with -std=c++26 -freflection, simdjson detects it by itself. Reflective reads of a struct use key selectors by default, which read the object in a single pass whatever the order of the keys.

I ran a demo on Compiler Explorer with GCC 16.2 and the simdjson 5.0.2 library. A struct with a string, an int, a bool, a nested struct and a vector is read from JSON whose keys match none of the member order. All fields come out right and the program exits with 0. The same run reports the integer 2^64 as a big integer, which the notes describe as new in 5.0.

The notes also report a 1.8x speedup. That figure is the author's measurement of DOM parsing a file full of escaped Unicode with GCC 16.1 on one Xeon core, simdjson 4.0 against 5.0. It is not a reflection result.

The demo does not show that the read took one pass; that comes from the documentation, which also still labels key selectors and simdjson::from experimental. I did not test clang-p2996, other simdjson versions, my own hardware, or performance. The June post on simdjson and reflection covers the writing side.

https://wrocpp.github.io/posts/simdjson-5-reflection-supported/

## Hashtags
#cpp #cplusplus #cpp26 #simdjson #json #reflection #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo and an AI-generated label. Headline reads "simdjson 5.0 reads struct fields in any key order" with a subtitle saying reflection is now an officially supported feature, shown by a GCC 16.2 run on Compiler Explorer. Citation footer: wro.cpp, 2026-10-18.

## Suggested post time
Sunday 2026-10-18, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
