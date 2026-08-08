# GCC 16.2 is out, LLVM 23.1 is nearly there, MSVC is still finishing C++23

## Body
Three months after C++26 was finalised, "which compiler should I use for it" has a clearer answer than it did in spring.

GCC 16.2 shipped on 7 August. It is a pure bug-fix release from the GCC 16 branch: more than a hundred regressions fixed against 16.1, no new language or library features. It is expected to become the default in Ubuntu 26.10 and Fedora 45, which matters more than the changelog, because it puts C++26 reflection in front of a lot of people who were not going looking for it.

LLVM 23.1 is still at rc2, posted 28 July, so late August is the realistic date for the final. When it lands it brings a substantial libc++ payload plus C++23 catch-up work like views::enumerate and the ranges::fold family.

Worth knowing about the split: some C++26 library features are ahead in libc++ and others in libstdc++, and neither is uniformly further along. When I checked in early August, GCC 16.1 had std::indirect, std::constant_wrapper and std::copyable_function while libc++ had none of the three, and libc++ advertised a feature-test macro for constant_wrapper it did not actually implement. Compile-test the feature, not the macro.

Reflection remains the sharpest difference: P2996 is in mainline GCC, and in Clang only via the Bloomberg fork.

MSVC is still finishing C++23 with no published C++26 timeline.

Full rundown: https://wrocpp.github.io/posts/gcc-16-2-toolchain-status/

Which toolchain are you actually stuck on?

## Hashtags
#cpp #cplusplus #gcc #llvm #cpp26 #toolchain

## Alt-text
A cream wro.cpp social card reading "For C++26 today, the answer is GCC", about the August 2026 toolchain status.

## Suggested post time
Monday 2026-08-17, 10:00 CET
Reason: Monday mid-morning CET opens the week for the EU audience.
