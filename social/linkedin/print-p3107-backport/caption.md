# C++26 rewrote std::print's internals and backported the fix

## Body
std::print's per-call atomicity extends to your own types. Give a type a std::formatter and printing it from many threads still yields whole lines, with nothing in your code synchronizing anything.

How print stays both safe and efficient is a C++26 story. As standardized in C++23, print was specified to format into a temporary std::string and write that whole string in one call. The temporary made non-interleaving obvious, but it also made the fast printf-style implementation (format straight into the stream buffer under its lock) nonconforming, and forced an allocation per call.

P3107, adopted for C++26, adds locking-aware entry points that write directly to the stream while holding its lock, and the plain print functions delegate to them. That recovers the efficiency without losing the guarantee.

The trap it dodges: a user formatter that itself prints to the same stream would deadlock while the lock is held. So formatters opt in via enable_nonlocking_formatter_optimization; the standard ones opt in automatically, and one that does not makes print take the safe path. Because it fixes behavior C++23 already promised, it was classified as a defect and recommended for backport. A C++26 change landing in your C++23 compiler.

Episode 5 of a series on concurrent I/O in C++.

https://wrocpp.github.io/posts/print-p3107-backport/

## Hashtags
#cpp #cplusplus #cpp26 #cpp23 #concurrency #stdprint #wg21 #moderncpp

## Alt-text
A cream wro.cpp card reading "A C++26 fix is being backported into C++23", on P3107 and std::print.

## Suggested post time
Friday 2026-10-02, 10:00 CET
Reason: morning CET; Friday series lane.
