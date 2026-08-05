# Chrome fixed 1,072 security bugs in two releases and 97% of its code is span-clean

## Body
Google published a Chrome security update with numbers big enough to be worth reporting on their own, and a strategy statement more candid than these posts usually are.

Chrome 149 and 150 together fixed 1,072 security bugs, more than the previous 23 milestones combined. A jump that size is not a collapse in code quality, it is a change in how many bugs are being found, driven by AI-assisted discovery and a reward programme that by March had already taken in more reports than all of 2025.

The number that matters to C++ programmers: 97% of first-party Chrome code now compiles cleanly under strict unsafe-buffer warnings. That is the result of a multi-year campaign Chromium calls spanification, replacing raw pointer-plus-length pairs with span so the length travels with the pointer. Clang's -Wunsafe-buffer-usage enforces it. Getting to 97% took organisational persistence rather than a technical breakthrough, which is exactly why other teams could copy it.

Then the sentence worth reading twice. Google writes that runtime mitigations "will hit diminishing marginal returns within the next few years", because runtime checks are inherently more expensive than compile-time guarantees. That is a fair summary of where C++ safety sits: every new bounds check buys less than the last one did.

Their answer is not to abandon C++, with 2,300 third-party dependencies in the tree, but to pair hardening with a Rust SDK for parsers and codecs.

https://wrocpp.github.io/posts/chrome-spanification/

Have you tried -Wunsafe-buffer-usage on a module of your own?

## Hashtags
#cpp #cplusplus #security #memorysafety #chrome #softwareengineering

## Alt-text
A cream wro.cpp social card reading "97% of Chrome compiles clean under span rules", about Chrome's security report and spanification.

## Suggested post time
Friday 2026-08-07, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
