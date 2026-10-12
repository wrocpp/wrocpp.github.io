# What C++23 and C++26 promise about a moved-from function wrapper

## Body
No standard function wrapper promises an empty source after a move. A probe shows libstdc++ 16.1 empties all three, while libc++ trunk keeps a copy in std::function and does not ship move_only_function or copyable_function yet. A small wrapper that states its own move works on both.

https://wrocpp.github.io/posts/function-wrappers-after-move/

## Hashtags
#cpp #cpp26 #cplusplus #libcxx #concurrency #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "No standard function wrapper promises an empty source" with a subtitle saying std::function, move_only_function and copyable_function leave the moved-from source unspecified. Citation footer: wro.cpp, 2026-10-24.

## Suggested post time
Saturday 2026-10-24, 16:00 UTC
Reason: second post of the day; the derive-eq-hash post holds the 08:00 UTC slot.
