# LLVM 23.1 shipped, and one of its changes is silent

## Body
LLVM 23.1.0 was released on 25 August, about two weeks after rc3.

Most of what landed in the C++ front end is the sort of thing you read once and forget. Expansion statements have partial support, so P1306R5 syntax is recognised although iterating expansion statements are still missing. P1857R3 modules dependency discovery is in, which matters to CMake and Ninja rather than to anything you write by hand. Structured bindings now propagate constexpr and constinit through tuple like initialisers. A batch of core issues landed: CWG1504, CWG1780, CWG2413, CWG727, CWG3135.

Then there is the one worth checking before you upgrade anything large.

Clang 23 is more aggressive about dead store elimination, and there is a new flag to switch it off: fno lifetime dse.

That the flag exists is the tell. Removing stores nobody reads is ordinary optimisation, right up to the point where the proof leans on lifetime rules a codebase quietly violates. Code that writes through a pointer to an object whose lifetime has ended, or that reuses storage without the standard blessing it, can lose those writes now where 22 kept them. Nothing warns you. The program simply behaves differently, usually in the parts that were already least well defined.

If a project moves to 23 and something goes strange in exactly the code you would not want to debug, try that flag first. If it helps, you have not found a compiler bug. You have found where your code depends on writes the standard does not require to happen.

Three other changes reject code that 22 accepted: export in module implementation partitions, _BitInt(N) deduced as size_t rather than int, and nested local classes declared in a different block scope from their parent.

Compiler Explorer does not carry 23.1 yet, so everything here is cited to the release notes rather than to something I ran.

https://wrocpp.github.io/posts/llvm-23-1-shipped/

Have you hit an optimisation that only showed up after a compiler bump?

## Hashtags
#cpp #cplusplus #clang #llvm #toolchain

## Alt-text
A wro.cpp social card reading "One change does not announce itself", about clang 23.1 eliding more dead stores.

## Suggested post time
Tuesday 2026-09-01, 09:00 CET
Reason: Weekday morning for a toolchain upgrade read.
