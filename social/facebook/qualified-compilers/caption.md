# Qualified C++ compilers in 2026

## Body
Which C++ compiler ships qualified for ISO 26262 (automotive), IEC 61508 (industrial), DO-178C (avionics), or IEC 62304 (medical)? The new wro.cpp page maps the 2026 vendor landscape: Green Hills MULTI, IAR EWARM, Wind River Diab, ARM Compiler 6, HighTec Clang, GCC + Validas. Plus the honest caveat: "qualified" is always (vendor, version, target, subset).

Subset note: MISRA C++:2023 superseded AUTOSAR C++14 in 2023; Adaptive AUTOSAR cites MISRA directly. Many tools still expose "AUTOSAR C++14" -- treat as alias.

The C++26 angle: a consteval predicate over `nonstatic_data_members_of(^^T)` encodes MISRA-class rules directly in the language. The compiler enforces them; you skip a separate analyzer qualification kit.

https://wrocpp.github.io/toolset/qualified-compilers/

## Hashtags
#cpp #cpp26 #functionalsafety #iso26262 #misra #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Qualified C++ compilers in 2026". Subhead: vendor matrix + reflection-driven MISRA lint. Citation: wro.cpp 2026-05-28.

## Suggested post time
Thursday 2026-05-28, 10:00 CET
Reason: Mid-week morning EU audience.
