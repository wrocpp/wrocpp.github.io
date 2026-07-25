# RealtimeSanitizer checks the promise that a function never blocks

## Body
Some C++ functions must never block. An audio callback has milliseconds before the speaker underruns. A control loop has a deadline set by physics. An interrupt handler has one set by the hardware. A correct answer delivered late is still a failure, and the usual causes are invisible in the source: a vector that quietly reallocates, a mutex that waits, a log line that touches the filesystem.

AddressSanitizer cannot help, because nothing is wrong in the memory-safety sense. The code is correct. It is just not allowed to do what it is doing.

RealtimeSanitizer (Clang, -fsanitize=realtime) checks exactly that. Mark a function [[clang::nonblocking]], which promises it will not call anything that might block, and RTSan verifies the promise at runtime with interposed allocator and locking primitives.

The demo marks an audio callback nonblocking and does two ordinary things: a push_back on an empty vector and a lock_guard. Both are reported. The first is the interesting one, because nothing in the line looks like an allocation:

  ERROR: RealtimeSanitizer: unsafe-library-call
  Intercepted call to real-time unsafe function `malloc` in real-time context!

The stack walks from the intercepted malloc back through six layers of standard-library inlining to the push_back that caused it. In code where a reviewer sees only a container append.

Run your realtime paths under RTSan in CI and a newly introduced allocation fails a test, instead of surfacing as an intermittent glitch a user reports months later.

Episode 3, running live: https://wrocpp.github.io/posts/verification-realtime-sanitizer/

Where in your codebase would this fire today?

## Hashtags
#cpp #cplusplus #realtime #audio #embedded #sanitizers #programming

## Alt-text
A cream wro.cpp social card reading "The malloc hiding inside your push_back", about Clang RealtimeSanitizer.

## Suggested post time
Thursday 2026-08-20, 10:00 CET
Reason: mid-morning CET on the post's pubDate for the EU audience.
