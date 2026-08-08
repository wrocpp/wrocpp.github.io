# GCC 16.2 is out, LLVM 23.1 is nearly there, MSVC is still finishing C++23

## Body
GCC 16.2 shipped on 7 August: a pure bug-fix release with more than a hundred regressions fixed and no new features. It is expected to become the default in Ubuntu 26.10 and Fedora 45, which puts C++26 reflection in front of a lot of people who were not looking for it.

LLVM 23.1 is still at rc2, so late August is realistic for the final. MSVC is still finishing C++23 with no C++26 date.

One thing worth knowing: the two standard libraries are ahead of each other in different places. GCC 16.1 has std::indirect, std::constant_wrapper and std::copyable_function while libc++ has none of the three, and libc++ even advertises a feature-test macro it does not implement. Compile-test the feature, not the macro.

If you want to write C++26 today, use GCC.

https://wrocpp.github.io/posts/gcc-16-2-toolchain-status/

## Hashtags
#cpp #cplusplus #gcc #llvm #cpp26

## Alt-text
A cream wro.cpp social card reading "For C++26 today, the answer is GCC", about the August 2026 toolchain status.

## Suggested post time
Monday 2026-08-17, 10:00 CET
Reason: Monday mid-morning CET for the EU audience.
