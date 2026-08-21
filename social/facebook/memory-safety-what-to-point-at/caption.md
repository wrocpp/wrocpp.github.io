# Answering the memory-safety question without profiles

## Body
The memory-safety question now arrives in vendor security questionnaires rather than conference talks, so the answer has to be a list of things you actually do.

C++26 did not settle it: profiles are still moving and contracts are being argued about rather than deployed. What exists today is less impressive and more useful.

A hardened standard library in production, measured at about 0.3% overhead across Google's fleet. Sanitizers gating the test suite. Warnings as errors, including the buffer ones that carried Chrome to 97% compliance. And types that remove the category rather than checking for it.

What not to claim: profiles, contracts as a safety feature, or that the compiler catches it.

What a team can actually point at: https://wrocpp.github.io/posts/memory-safety-what-to-point-at/

## Hashtags
#cpp #cplusplus #security #programming

## Alt-text
A wro.cpp card about practical C++ memory-safety controls.

## Suggested post time
Friday 2026-10-16, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
