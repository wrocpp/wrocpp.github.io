# Structured concurrency: what std::future never had

## Body
A std::future is a one-shot dead end -- launch it, get() it once, and combining two means manual threads and locks.

C++26's std::execution fixes that. "senders" compose: when_all(a, b) runs both pieces concurrently and finishes when both are done, with no mutex and no thread to join by hand. And because the result is itself a sender, you can keep building on it -- even swap the thread pool for a GPU scheduler and the same code runs on the device.

One click to run it (GCC 16.1 + clang):

https://wrocpp.github.io/posts/structured-concurrency/

## Hashtags
#cpp #cpp26 #programming #concurrency #wrocpp

## Alt-text
A dark wro.cpp social card with the line "A std::future is a dead end. A C++26 sender is a node you keep building a graph from."

## Suggested post time
Tuesday 2026-06-30, 10:00 CET
Reason: matches the publish date; weekday mid-morning for reach.
