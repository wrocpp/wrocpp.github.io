# Converting between std::function and copyable_function nests them

## Body
C++ now has a small family of type-erased callable wrappers. std::function copies. move_only_function does not. copyable_function is the fixed-up copyable one. function_ref borrows instead of owning. Having four is defensible. The trap is what happens at the boundary between two of them.

None of these wrappers recognises any of the others. When you convert a std::function into a copyable_function, the target does not look inside to find the original lambda and re-erase it. It sees an arbitrary callable that happens to be a std::function, and stores a copy of that whole wrapper. Convert back and you wrap the wrapper.

I timed it. Ten thousand calls through a fresh std::function, then 200 round trips through copyable_function, then the identical calls again:

  before : 19 us
  after  : 8889 us
  slowdown : 467x

The checksums match, so the code stays correct while getting arbitrarily slower. Nothing warns, and the type never changes: it is still std::function<int(int)> at the end.

Nobody writes a 200-iteration conversion loop. The realistic version is architectural: a handler stored as std::function in one subsystem, passed to another that standardised on copyable_function, registered back into a third. Three conversions per registration is nothing, until the registration happens per frame or per request.

Two rules avoid it. Pick one owning wrapper per codebase for interfaces that cross module boundaries. And take callbacks by function_ref when you only invoke and do not store, since there is nothing to convert and no wrapper to nest.

https://wrocpp.github.io/posts/function-wrapper-explosion/

Timings vary between runs, so treat the multiplier as one representative run.

## Hashtags
#cpp #cplusplus #cpp26 #performance #stdlib #programming

## Alt-text
A cream wro.cpp social card reading "200 conversions made the calls 467x slower", about nesting std::function and copyable_function.

## Suggested post time
Monday 2026-08-10, 10:00 CET
Reason: Monday mid-morning CET opens the week for the EU audience.
