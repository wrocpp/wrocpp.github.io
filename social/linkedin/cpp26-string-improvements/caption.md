# Three small C++26 string fixes you will use every day

## Body
C++26's headline features get the attention, but it also closes three string-library paper cuts you hit constantly:

1. string + string_view finally compiles (P2591), in both orders. No more building a temporary just to concatenate.
2. stringstream straight from a string_view (P2495). No temporary copy.
3. bitset from a string_view (P2697), and no more .data() null-termination traps.

None are flashy. All of them delete boilerplate and a hidden allocation you have been writing for years, and the string_view constructors close a real correctness hazard. All mainline, already shipping in GCC and Clang.

Verified on GCC 16.1 and the Bloomberg clang-p2996 fork.
https://wrocpp.github.io/posts/cpp26-string-improvements/

## Hashtags
#cpp #cpp26 #stdlib #stringview #programming #moderncpp

## Alt-text
A wro.cpp card listing three C++26 string and string_view improvements.

## Suggested post time
2026-07-10, 10:00 CET
