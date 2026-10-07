# Registration and test discovery from reflection

## Body
A test runner printed "7 cases, 0 failed". One file's tests had run twice and another file's three tests had not run at all. The linker said nothing, and -Wodr under LTO said nothing either.

The runner finds its tests with members_of on a namespace and an annotation. That works inside one translation unit. Across files each one needs a registrar line, and the registrar's [] {} argument is mandatory, because without it the constructor is one shared inline function whose body depends on the file that instantiated it. A plain static library drops the registrars as well: I got 1 case instead of 7 until I linked the whole archive, on GNU ld 2.44 (Linux aarch64, Docker) and on macOS ld64.

The same machinery registers a type with EnTT's runtime reflection in one line instead of 8, 23 or 53 for 5, 20 or 50 members. The post compares this with how Catch2 and GoogleTest register tests, from their current docs and sources, and lists what was not tested: no clang-p2996, no x86-64 machine of my own, and only two linkers.

https://wrocpp.github.io/posts/register-types-and-find-tests-from-reflection/

## Hashtags
#cpp #cpp26 #reflection #testing #entt #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "The runner said 7 passed. Three tests never ran." with a subtitle saying that one missing lambda made a reflection-based test registrar run one file's tests twice and skip the other's, with no warning. Citation footer: wro.cpp, 2026-11-13.

## Suggested post time
Friday 2026-11-13, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
