# A new proposal deletes your enum bitmask boilerplate

## Body
A scoped enum is the right type for a flag set, until you want to combine two flags. enum class takes the bitwise operators away, so every project writes them back: operator|, &, ^, ~, the compound forms, a has() helper. Eight-ish functions per bitmask enum, forever.

P4313 (Guterman and Williams, 2026-07 mailing) proposes deleting that block. Mark the enum with an attribute, enum class [[std::bitmask_type]], and the language supplies the operators, with no implicit conversion between different bitmasks. The demo is the boilerplate it removes, running today on GCC 16.1.

It is an early proposal, but it targets a papercut every codebase has: https://wrocpp.github.io/posts/bitmask-enums/

## Hashtags
#cpp #cplusplus #wg21 #programming #softwareengineering

## Alt-text
A cream wro.cpp social card reading "Stop hand-writing enum flag operators", about P4313 and enum class [[std::bitmask_type]].

## Suggested post time
Friday 2026-07-31, 10:00 CET
Reason: mid-morning CET for the EU audience on the post's pubDate.
