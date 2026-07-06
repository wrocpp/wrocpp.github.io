# Hello, sender: your first std::execution pipeline

## Body
C++26 has three big features: reflection, contracts, and std::execution. The first two get the attention. std::execution (the new standard way to write asynchronous and parallel code) is the one most projects will use first.

The idea: a "sender" describes work lazily. You chain steps with the pipe operator, and nothing runs until you wait for the result. Unlike a std::future (eager, use-once), a sender is a recipe you keep building on.

Here is the smallest example that actually runs, one click on Compiler Explorer (GCC 16.1 and clang):

https://wrocpp.github.io/posts/hello-sender/

## Hashtags
#cpp #cpp26 #programming #softwaredevelopment #wrocpp

## Alt-text
A dark wro.cpp social card titled "Your first C++26 sender, in 12 lines", introducing the std::execution async model.

## Suggested post time
Sunday 2026-06-28, 10:00 CET
Reason: matches the post's publish date; mid-morning weekend slot for broader reach.
