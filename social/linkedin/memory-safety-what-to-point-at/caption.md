# Answering the memory-safety question without profiles

## Body
The memory-safety question has changed shape. It used to arrive in conference talks, where the answer could be a position. Now it arrives in vendor security questionnaires, where the answer has to be a list of things you actually do.

C++26 did not settle it. The profiles work is still moving, contracts are being argued about rather than deployed, and neither is in a compiler you can ship against this quarter. So the honest answer is not a standard feature. It is a set of things that already work.

A hardened standard library, switched on in production. libc++ and libstdc++ both ship modes that turn out-of-range container access into a trap rather than undefined behaviour, at roughly 0.3% overhead measured across Google's fleet. That is a number you can put in a questionnaire.

Sanitizers in CI, not just on a developer's laptop. Too slow for most production builds and entirely affordable on a test suite. "We run ASan and UBSan on every pull request" is a concrete control; "we are careful" is not.

Warnings promoted to errors, including the buffer ones. Chrome reached 97% compliance with -Wunsafe-buffer-usage while fixing over a thousand security bugs.

Types that make the bug unrepresentable: span instead of pointer and length, string_view where lifetimes allow, C++26's indirect for the PImpl case.

What not to claim: profiles, because they are not in a shipping compiler. Contracts as a safety feature, because a group including Stroustrup is arguing they should be removed partly on the grounds that they do not deliver safety guarantees. And that the compiler catches it, because plenty of undefined behaviour produces no warning at all.

The reason to write the list down is not compliance theatre. The alternative answer, that C++ is memory-unsafe and always will be, is the one being written down for you.

What a team can actually point at: https://wrocpp.github.io/posts/memory-safety-what-to-point-at/

## Hashtags
#cpp #cplusplus #security #memorysafety #softwareengineering

## Alt-text
A wro.cpp card reading "Answering the memory-safety question without profiles", about practical C++ safety controls.

## Suggested post time
Friday 2026-10-16, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
