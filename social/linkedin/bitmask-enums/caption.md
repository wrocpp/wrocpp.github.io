# A new proposal deletes your enum bitmask boilerplate

## Body
A scoped enum is the right type for a set of flags: named values, no implicit conversion to int, its own namespace. Then you want to combine two flags, and enum class takes the bitwise operators away, so you write them back. Every project has the block: operator|, operator&, operator^, operator~, the compound-assignment forms, a has() helper. Eight-ish functions, once per bitmask enum, forever.

P4313 "Bitmask operations for enums" (Iliya Guterman and Anthony Williams, in the 2026-07 mailing) proposes deleting that block. You opt a scoped enum into bitmask behavior with an attribute, enum class [[std::bitmask_type]] Permission { ... }, and the language supplies the operators. Two design points make it more than a macro: no implicit conversion, so a Permission and a Color bitmask never mix, and values keep their enum type through every operation instead of decaying to the underlying integer.

The demo is the code the proposal would let you throw away. It compiles today on GCC 16.1 (the attribute does not exist yet, so the operators are hand-written) and prints the result of combining and testing flags.

It is an R0, so it will change as it moves through the committee, but it targets a universal papercut with the design library authors have hand-rolled with concepts for years: https://wrocpp.github.io/posts/bitmask-enums/

How many hand-rolled flag-operator blocks are in your codebase right now?

## Hashtags
#cpp #cplusplus #wg21 #cpp29 #programming #softwareengineering

## Alt-text
A cream wro.cpp social card reading "Stop hand-writing enum flag operators", about P4313 proposing enum class [[std::bitmask_type]].

## Suggested post time
Friday 2026-07-31, 10:00 CET
Reason: post lands on its pubDate; mid-morning CET for the EU C++ audience.
