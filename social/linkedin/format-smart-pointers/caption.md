# Why you can't std::format a smart pointer (and how to anyway)

## Body
A question went around r/cpp: std::cout << a unique_ptr works, but std::println("{}", that_unique_ptr) is ill-formed. There is no std::formatter for smart pointers. Oversight?

No -- it is deliberate. std::format only makes void*, const void*, and nullptr_t formattable among pointers; an arbitrary int* is disabled on purpose, so you never print an address when you meant a value. Smart-pointer formatters were proposed (P1636, 2019) and LEWG asked for them to be removed; the follow-up P2930 adds optional/variant/expected/any and still leaves smart pointers out. The operator<< asymmetry is just history -- shared_ptr's << (C++11) and unique_ptr's << (C++20) inherit the "pointers print their address" convention.

Three ways to format a smart pointer today, each verified on Compiler Explorer: cast .get() to void* (plus the new C++26 P2510 spec), print the pointee *p null-safely, or write a small formatter for your own pointee type.

https://wrocpp.github.io/posts/format-smart-pointers/

Should the standard ever add it -- and as the address, or the pointee?

## Hashtags
#cpp #cpp26 #stdformat #smartpointers #cpplang #wrocpp

## Alt-text
A dark wro.cpp social card with the line "std::format won't print a smart pointer. That is deliberate, not an oversight."

## Suggested post time
Saturday 2026-07-04, 10:00 CET
Reason: matches the publish date; a weekend slot fits a discussion-style post that invites replies.
