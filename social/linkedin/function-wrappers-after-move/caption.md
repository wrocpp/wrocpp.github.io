# What C++23 and C++26 promise about a moved-from function wrapper

## Body
The standard does not promise an empty source after a move for std::function, std::move_only_function or std::copyable_function. All three say the source is in a valid state with an unspecified value.

A probe on Compiler Explorer shows what that means today. libstdc++ 16.1 empties all three. libc++ trunk keeps a copy in std::function and does not ship the other two. std::function_ref is on both, but it does not own the callable, so it cannot carry a queued task.

The post ends with a small wrapper class that states its own move with std::exchange. The probe shows it leaving an empty source on both libraries.

https://wrocpp.github.io/posts/function-wrappers-after-move/

## Hashtags
#cpp #cpp26 #cplusplus #libcxx #concurrency #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "No standard function wrapper promises an empty source" with a subtitle saying std::function, move_only_function and copyable_function leave the moved-from source unspecified. Citation footer: wro.cpp, 2026-10-24.

## Suggested post time
Saturday 2026-10-24, 16:00 UTC
Reason: second post of the day; the derive-eq-hash post holds the 08:00 UTC slot.
