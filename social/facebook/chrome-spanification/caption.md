# Chrome fixed 1,072 security bugs in two releases

## Body
Chrome 149 and 150 together fixed 1,072 security bugs, more than the previous 23 milestones combined. That is not a collapse in code quality, it is a change in how many bugs are being found.

The number for C++ programmers: 97% of first-party Chrome code now compiles cleanly under strict unsafe-buffer warnings. That is the result of spanification, replacing raw pointer-plus-length pairs with span so the length travels with the pointer, enforced by Clang's -Wunsafe-buffer-usage.

Google also says plainly that runtime mitigations will hit diminishing returns within a few years, because runtime checks cost more than compile-time guarantees. Their answer is hardened C++ plus Rust for parsers and codecs.

https://wrocpp.github.io/posts/chrome-spanification/

## Hashtags
#cpp #cplusplus #security #memorysafety #programming

## Alt-text
A cream wro.cpp social card reading "97% of Chrome compiles clean under span rules", about Chrome security and spanification.

## Suggested post time
Friday 2026-08-07, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
