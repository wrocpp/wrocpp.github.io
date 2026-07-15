# std::osyncstream makes concurrent output atomic

## Body
Last time, three threads logging to std::cout shredded each other's lines. C++20 fixes it with one wrapper: std::osyncstream.

Give each thread its own osyncstream(std::cout). You write into it exactly like cout, but nothing reaches the real stream until the osyncstream is destroyed. Then the whole accumulated block transfers in one shot. Underneath is a basic_syncbuf holding a private buffer; every << appends there and touches the destination not at all, until emit. So two threads can be mid-line at once, and their lines only meet at the destination, one whole block after another.

The idiomatic form is a temporary: std::osyncstream(std::cout) << ... and a newline. The semicolon destroys it, which emits the line atomically.

There is one sharp edge. The no-interleave guarantee holds only if every writer to that buffer uses a syncstream. One stray raw cout next to the synced threads can still land mid-block. osyncstream coordinates with other syncstreams; it does not lock cout against the world.

Episode 2 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/osyncstream/

## Hashtags
#cpp #cplusplus #cpp20 #concurrency #multithreading #iostream #logging #moderncpp

## Alt-text
A cream wro.cpp card reading "The C++20 line that un-garbles your logs", on std::osyncstream.

## Suggested post time
Friday 2026-09-11, 10:00 CET
Reason: morning CET; the series runs on Fridays.
