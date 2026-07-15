# std::endl is a hidden flush, and clang-tidy flags it

## Body
std::endl looks like a fancy newline. It is a newline plus a flush, and the flush is the part that costs you. On a path that writes many lines, reflexive endl turns each line into a forced trip to the operating system.

The demo wraps a streambuf that counts flushes. Five lines ending in a newline cause zero flushes; the characters sit in the buffer. Five lines ending in std::endl cause five, because endl is a newline followed by std::flush.

The flush is not always waste; it is what makes output survive a crash. cout is buffered, so a crash with unwritten lines loses them. cerr has unitbuf set and flushes every operation, which is why error output tends to survive a crash that swallows normal output. So the rule is intent: plain newline on the hot path, deliberate flush at a checkpoint or on the error path.

One caveat: flush hands bytes to the OS, not to the disk. It protects against a crashing process; surviving a power cut is fsync's job.

clang-tidy ships performance-avoid-endl for exactly this, and it is a good default to turn on.

Episode 7 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/endl-flush-crash-logs/

## Hashtags
#cpp #cplusplus #performance #iostream #logging #cleancode #moderncpp

## Alt-text
A cream wro.cpp card reading "std::endl is a performance bug", on flush semantics.

## Suggested post time
Friday 2026-10-16, 10:00 CET
Reason: morning CET; Friday series lane.
