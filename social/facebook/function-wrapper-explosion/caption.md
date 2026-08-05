# Converting between std::function and copyable_function nests them

## Body
C++ has four type-erased callable wrappers now, and none of them recognises any of the others. Converting a std::function into a copyable_function does not find the lambda inside and re-erase it. It stores a copy of the whole wrapper. Convert back and you wrap the wrapper.

I timed it: 10k calls took 19 us before, and 8889 us after 200 round trips. A 467x slowdown, with matching checksums and no warning, and the type is still std::function<int(int)> at the end.

Nobody writes that loop deliberately. The realistic version is a handler crossing three subsystems that each picked a different wrapper. Fix: standardise on one owning wrapper, and take callbacks by function_ref when you only invoke and do not store.

https://wrocpp.github.io/posts/function-wrapper-explosion/

## Hashtags
#cpp #cplusplus #cpp26 #performance #programming

## Alt-text
A cream wro.cpp social card reading "200 conversions made the calls 467x slower", about nesting callable wrappers.

## Suggested post time
Monday 2026-08-10, 10:00 CET
Reason: Monday mid-morning CET for the EU audience.
