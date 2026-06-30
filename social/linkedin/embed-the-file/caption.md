# Embed a file at compile time: #embed in C++26

## Body
Baking a file into a binary has always meant a side quest: run xxd -i, commit (or generate) the resulting header, wire a CMake custom command to keep it fresh, and hope nobody hand-edits the generated array.

C++26 deletes the ritual. It adopts C23's #embed directive: the preprocessor reads the file and expands it into a list of byte values, right where you write it. Drop it straight into a static constexpr unsigned char[] and the bytes are baked into the program image -- no file to open at runtime, no path to get wrong, no I/O to fail.

The contrast is the whole point. xxd -i produced an artifact that could silently drift from the file it came from. #embed has no intermediate: the file is the source of truth, read fresh on every build. GCC 16.1 ships it today.

Runnable on Compiler Explorer:

https://wrocpp.github.io/posts/embed-the-file/

## Hashtags
#cpp #cpp26 #embed #preprocessor #cpplang #buildsystems #wrocpp

## Alt-text
A dark wro.cpp social card showing the stat "0 codegen steps" for the C++26 #embed directive.

## Suggested post time
Thursday 2026-07-02, 10:00 CET
Reason: matches the publish date; weekday mid-morning slot.
