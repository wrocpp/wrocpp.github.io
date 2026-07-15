# std::print does not tear the way std::cout does

## Body
osyncstream needs every writer to cooperate. The static mutex needs a lock around each write. C++23's std::print gives you the common case for free.

A single std::print or std::println call does not interleave with other calls, the printf-style atomicity that std::cout never had. No syncstream, no mutex: one call, one whole line. It works because print formats into a temporary string and writes it in one operation while the C stream holds its lock.

The demo shows the guarantee and its edge. Three threads calling println once per line produce clean, whole lines. But when one logical line is split into two calls (print for the prefix, println for the rest), each call is atomic and nothing binds them, so another thread's line lands in the gap. The prefixes and suffixes splice exactly like the raw cout version.

The rule for a logger: build each line in a single print call, all arguments in one format string. Split it across calls and you are back to needing a lock or a syncstream to group them.

Episode 4 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/print-atomic-per-call/

## Hashtags
#cpp #cplusplus #cpp23 #concurrency #stdprint #iostream #moderncpp

## Alt-text
A cream wro.cpp card reading "std::print quietly fixed what iostreams never did", on per-call output atomicity.

## Suggested post time
Friday 2026-09-25, 10:00 CET
Reason: morning CET; Friday series lane.
