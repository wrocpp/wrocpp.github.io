# C++26 rewrote std::print's internals and backported the fix

## Body
std::print never interleaves a single call, even for your own std::formatter types. The story behind that is a C++26 change.

C++23 specified print to format into a temporary string, which made non-interleaving obvious but blocked the fast printf-style implementation. P3107 (C++26) adds locking-aware writes straight to the stream, with a formatter opt-in so a formatter that itself prints cannot deadlock.

Because it corrects behavior C++23 already promised, it was classified as a defect fix and recommended for backport into C++23.

Episode 5 of a series on concurrent I/O.

https://wrocpp.github.io/posts/print-p3107-backport/

## Hashtags
#cpp #cplusplus #cpp26 #concurrency #programming
