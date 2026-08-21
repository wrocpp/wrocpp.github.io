# Boost and Abseil start deleting their C++14 shims

## Body
Two release notes went out nine days apart in August, and they point the same way.

Boost 1.92.0 on 12 August, in the Heap and Lockfree section: this release is the last to support C++14, and future releases will require C++17. Abseil's LTS 20260817.0 on 18 August, under breaking changes: absl::void_t is deprecated, use C++17's std::void_t directly.

Neither is a headline feature. Together they mark the point where two very widely deployed libraries stopped carrying code whose only purpose was serving people who could not yet assume C++17.

void_t is a good example of what a shim actually cost, because it looks trivial and is not. It is the machinery behind the detection idiom, and the obvious one-line spelling does not reliably work: unused parameters in an alias template were not required to participate in substitution, so detection could silently always succeed. That is CWG 1558, and until compilers implemented the resolution, libraries shipped a workaround that routed the pack through a class template instead.

That extra indirection is the shim. It exists for compilers that no longer matter, and it is what gets deleted when a floor moves.

GoogleTest got there first, which is worth being accurate about. Its 1.16 was the last branch supporting C++14 and 1.17 raised the floor back in April 2025. So this is not three libraries deciding something in August. It is Boost and Abseil arriving where GoogleTest already was, sixteen months later.

The direction of the dependency is the interesting part. For a decade the standard library was the laggard and third party libraries filled the gaps ahead of it: void_t, optional, string_view, span. Now the standard has caught up and the gap fillers are being removed.

The demo compiles three spellings of void_t side by side on GCC 16.2. Switch it to std=c++14 and it stops at the first one.

https://wrocpp.github.io/posts/cpp14-shims-deleted/

Are you still building anything at C++14?

## Hashtags
#cpp #cplusplus #boost #abseil #cpp17

## Alt-text
A wro.cpp social card reading "The C++14 shims are being deleted", about Boost 1.92 and Abseil dropping pre-C++17 compatibility code.

## Suggested post time
Thursday 2026-09-03, 09:00 CET
Reason: Weekday morning for a toolchain and dependencies read.
