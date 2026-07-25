# RealtimeSanitizer checks the promise that a function never blocks

## Body
Some C++ functions must never block: audio callbacks, control loops, interrupt handlers. A correct answer delivered late is still a failure, and the causes are invisible in the source. A vector that quietly reallocates. A mutex that waits.

AddressSanitizer cannot help, because nothing is wrong in the memory-safety sense. The code is correct, it is just not allowed to do what it is doing.

Mark a function [[clang::nonblocking]] and RealtimeSanitizer verifies the promise at runtime. In the demo it catches the malloc hiding inside a plain push_back, and the stack walks back through six layers of standard-library inlining to the line that caused it.

Episode 3, running live: https://wrocpp.github.io/posts/verification-realtime-sanitizer/

## Hashtags
#cpp #cplusplus #realtime #embedded #programming

## Alt-text
A cream wro.cpp social card reading "The malloc hiding inside your push_back", about Clang RealtimeSanitizer.

## Suggested post time
Thursday 2026-08-20, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
