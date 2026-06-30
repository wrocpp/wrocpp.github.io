# Embed a file at compile time: #embed in C++26

## Body
Putting a file inside your binary used to mean xxd -i, a generated header, and a build step that drifts out of sync.

C++26 adopts C23's #embed: the compiler reads the file at build time and drops its bytes right into your array -- no codegen, no glue. The file itself is the source of truth, read fresh every build. GCC 16.1 has it now.

One click to try it:

https://wrocpp.github.io/posts/embed-the-file/

## Hashtags
#cpp #cpp26 #programming #wrocpp

## Alt-text
A dark wro.cpp social card showing the stat "0 codegen steps" for the C++26 #embed directive.

## Suggested post time
Thursday 2026-07-02, 10:00 CET
Reason: matches the publish date; weekday mid-morning slot.
