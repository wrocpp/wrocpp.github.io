# The sanitizers run live on Compiler Explorer

## Body
The sanitizers are the cheapest way to catch memory bugs, undefined behavior, and data races in C++, and you do not need a local setup to use them. AddressSanitizer, UBSan, and ThreadSanitizer all run right in Compiler Explorer.

Add one -fsanitize flag and the report prints in the browser: the faulting line for a heap overflow, the exact operands for a signed overflow, both stacks for a data race. Because it is a shareable link, the report becomes something you can send instead of explain.

Three flags, three classic bugs, all running: https://wrocpp.github.io/posts/sanitizers-on-ce/

## Hashtags
#cpp #cplusplus #debugging #programming #softwareengineering

## Alt-text
A cream wro.cpp social card reading "One flag, and the bug names its own line", about sanitizers running on Compiler Explorer.

## Suggested post time
Thursday 2026-07-23, 10:00 CET
Reason: mid-morning CET for the EU audience on the post's pubDate.
