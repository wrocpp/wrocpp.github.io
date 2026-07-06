# Why you can't std::format a smart pointer (and how to anyway)

## Body
Spotted on r/cpp: you can stream a unique_ptr with std::cout <<, but std::format / std::println rejects it. There is no formatter for smart pointers. Bug?

No, it is a deliberate choice. std::format only formats void* among pointers (so you never print an address by accident), and the committee twice chose not to add smart-pointer formatters. The old << just predates that stricter design.

The post shows three ways to do it today (cast to void* with the new C++26 options, print the pointee, or write a tiny formatter), all runnable in one click:

https://wrocpp.github.io/posts/format-smart-pointers/

## Hashtags
#cpp #cpp26 #programming #wrocpp

## Alt-text
A dark wro.cpp social card with the line "std::format won't print a smart pointer. That is deliberate, not an oversight."

## Suggested post time
Saturday 2026-07-04, 10:00 CET
Reason: matches the publish date; weekend discussion slot.
