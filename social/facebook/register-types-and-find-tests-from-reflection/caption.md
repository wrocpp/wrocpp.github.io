# Registration and test discovery from reflection

## Body
A reflection-based test runner reported 7 passed while three tests never ran and the other file's tests ran twice. Neither the compiler nor the linker warned. The cause was a missing [] {} in one registrar line.

The post builds the runner, shows the trap and the static library case, and registers a type with EnTT in one line. It was tested on GCC 16.2 only, and the post lists the rest.

https://wrocpp.github.io/posts/register-types-and-find-tests-from-reflection/

## Hashtags
#cpp #cpp26 #reflection #testing #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "The runner said 7 passed. Three tests never ran." with a subtitle saying that one missing lambda made a reflection-based test registrar run one file's tests twice and skip the other's, with no warning. Citation footer: wro.cpp, 2026-11-13.

## Suggested post time
Friday 2026-11-13, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
