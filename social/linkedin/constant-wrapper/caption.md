# std::constant_wrapper carries a compile-time value as an argument

## Body
C++ has always had two places to put a value, with a wall between them. A template parameter is known at compile time and usable in a static_assert or an array extent, but you cannot pass one as a function argument. A function argument can be passed around freely but is a runtime value, so it cannot be used where a constant is required.

The workaround everyone knows is std::integral_constant, which has existed since C++11 and is exactly this idea in its most spartan form: an empty type whose type carries the value.

C++26 finishes the job with std::constant_wrapper. The difference is that it behaves like the value it holds. Adding two constant_wrappers does not give you an int, it gives you another constant_wrapper, so the value never falls out of the type system and the result still satisfies static_assert and still works as an array extent. That is what integral_constant could not do.

The motivating use is APIs that need a compile-time value but want to look like normal functions. Instead of matrix.get<2, 3>() with template arguments that are awkward to forward, you write matrix.get(cw<2>, cw<3>), which forwards through wrappers, works in a fold expression, and can be defaulted.

One availability note that is its own lesson. GCC 16.1 ships it. libc++ 24 defines the feature-test macro at a newer value but does not actually provide the facility, so a macro check reports it present on a toolchain where it is not. Compile-test the feature, not the macro.

https://wrocpp.github.io/posts/constant-wrapper/

## Hashtags
#cpp #cplusplus #cpp26 #metaprogramming #constexpr #programming

## Alt-text
A cream wro.cpp social card reading "A compile-time value you can pass as an argument", about C++26 std::constant_wrapper.

## Suggested post time
Saturday 2026-08-15, 10:00 CET
Reason: weekend mid-morning for a metaprogramming read.
