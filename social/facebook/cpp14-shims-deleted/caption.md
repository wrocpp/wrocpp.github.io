# Boost and Abseil start deleting their C++14 shims

## Body
Two release notes nine days apart in August point the same way.

Boost 1.92.0 on 12 August: Heap and Lockfree say this is the last release supporting C++14. Abseil's August LTS deprecates absl::void_t and tells you to use the standard std::void_t instead.

void_t shows what a shim actually cost. It is the machinery behind the detection idiom, and the obvious one line version did not reliably work, so libraries shipped a workaround routing the parameter pack through a class template. That indirection exists for compilers that no longer matter.

GoogleTest got there first: 1.16 was its last C++14 branch and 1.17 raised the floor in April 2025. So this is Boost and Abseil arriving where GoogleTest already was.

For a decade third party libraries filled gaps ahead of the standard. Now the standard has caught up and the gap fillers are going away.

https://wrocpp.github.io/posts/cpp14-shims-deleted/

## Hashtags
#cpp #cplusplus #boost #abseil #cpp17

## Alt-text
A wro.cpp social card reading "The C++14 shims are being deleted", about Boost 1.92 and Abseil dropping pre-C++17 compatibility code.

## Suggested post time
Thursday 2026-09-03, 09:00 CET
Reason: Weekday morning for a toolchain and dependencies read.
