# Hello, sender: your first std::execution pipeline

## Body
C++26 shipped three tentpole features. Reflection and contracts get the headlines. The third, std::execution, is the one most service codebases will reach for first, and it is the least talked about.

std::execution (P2300) is the standard model for asynchronous and parallel work: senders, receivers, schedulers. A sender is a lazy description of work, not the work itself. "just(21)" produces a value; "then(f)" transforms it; operator| chains them. Nothing runs until "sync_wait" drives the pipeline and hands back the result.

That laziness is the point. A std::future is eager and one-shot. The work is already running and you can only get() it once. A sender is a recipe you can keep composing before anyone lights the stove.

The shipping standard-library headers do not carry the sender machinery yet (June 2026), so the runnable example uses NVIDIA's stdexec reference implementation (the same code the wording was distilled from). One click compiles and runs it on Compiler Explorer, on both GCC 16.1 and clang-p2996.

Read the 12-line walkthrough: https://wrocpp.github.io/posts/hello-sender/

What are you reaching for std::execution to replace first: thread pools, futures, or hand-rolled callback chains?

## Hashtags
#cpp #cpp26 #stdexecution #asynchronous #concurrency #cpplang #wrocpp

## Alt-text
A dark wro.cpp social card titled "Your first C++26 sender, in 12 lines", introducing the std::execution async model.

## Suggested post time
Sunday 2026-06-28, 10:00 CET
Reason: matches the post's publish date; Sunday mid-morning catches European C++ developers before the work week.
