# std::constant_wrapper carries a compile-time value as an argument

## Body
C++ has two places to put a value, with a wall between them. A template parameter is a compile-time value you cannot pass as an argument. A function argument is a runtime value you cannot use where a constant is required.

C++26's std::constant_wrapper crosses that line. It is an empty object carrying a compile-time value, and crucially it survives arithmetic: adding two of them gives another constant_wrapper, not an int, so the result still satisfies static_assert and still works as an array extent. That is what std::integral_constant could never do.

The use is APIs that need a constant but want to look like ordinary functions: matrix.get(cw<2>, cw<3>) instead of template arguments that are awkward to forward.

One caveat worth its own lesson: GCC 16.1 ships it, but libc++ defines the feature-test macro without providing the facility. Compile-test the feature, not the macro.

https://wrocpp.github.io/posts/constant-wrapper/

## Hashtags
#cpp #cplusplus #cpp26 #metaprogramming #programming

## Alt-text
A cream wro.cpp social card reading "A compile-time value you can pass as an argument", about std::constant_wrapper.

## Suggested post time
Saturday 2026-08-15, 10:00 CET
Reason: weekend mid-morning for a metaprogramming read.
