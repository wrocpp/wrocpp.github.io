# LLVM 23.1 shipped, and one of its changes is silent

## Body
LLVM 23.1.0 shipped on 25 August, about two weeks after rc3.

Most of the C++ front end changes are quiet: partial expansion statements, modules dependency discovery, structured bindings propagating constexpr through tuple like initialisers, and a batch of core issue fixes.

One is worth checking before a big upgrade. Clang 23 elides more dead stores than 22 did, and there is a new flag to turn it off: fno lifetime dse.

That the flag exists is the tell. Code that writes through an object whose lifetime has ended can lose those writes now, and nothing warns you. The program just behaves differently, usually in the code you least want to debug.

If it fixes your problem, you have not found a compiler bug. You have found where your code depends on writes the standard never required.

https://wrocpp.github.io/posts/llvm-23-1-shipped/

## Hashtags
#cpp #cplusplus #clang #llvm #toolchain

## Alt-text
A wro.cpp social card reading "One change does not announce itself", about clang 23.1 eliding more dead stores.

## Suggested post time
Tuesday 2026-09-01, 09:00 CET
Reason: Weekday morning for a toolchain upgrade read.
