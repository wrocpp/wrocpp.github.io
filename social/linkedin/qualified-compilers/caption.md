# Qualified C++ compilers in 2026: the vendor map for ISO 26262 / IEC 61508 / DO-178C / IEC 62304

## Body
"Use a qualified compiler" is the line that separates C++ in a side project from C++ in a brake controller. ISO 26262 Part 8 Section 11 demands a Software Tool Confidence Level (TCL) argument for every tool whose output ends up in a safety-related item. IEC 61508, DO-178C, and IEC 62304 impose equivalent obligations. The 2026 wro.cpp toolset entry maps the live vendor landscape across all four standards.

The matrix at a glance: **Green Hills MULTI / IAR EWARM / Wind River Diab** -- proprietary, ASIL D + SIL 4 + DO-178C Level A. **ARM Compiler 6** -- ASIL D with the Arm Functional Safety package. **HighTec Clang** -- the LLVM newcomer, certified ASIL D + SIL 3 since 2024. **GCC + Validas CTS** -- the open-source path with a commercial qualification overlay.

The honest caveat: "qualified compiler" is always a (vendor, version, target triple, language subset) tuple. For automotive C++ the subset is **MISRA C++:2023** -- which superseded AUTOSAR C++14 in 2023; Adaptive AUTOSAR now references MISRA directly. Many tools still expose an "AUTOSAR C++14" profile name for backward compatibility -- treat it as an alias and cite MISRA in new safety cases.

The C++26 reflection angle: every additional analyzer in your pipeline needs its own qualification kit. A `consteval` predicate that walks `nonstatic_data_members_of(^^T)` and `static_assert`s MISRA C++:2023 Rule 11.0.1 (data members must be private) is part of the language toolchain's TCL-1 argument. A clang-tidy or Coverity run enforcing the same rule is a TCL-3 tool. **Moving rules into the type system shrinks the qualification surface.** That changes how kit costs scale with project size.

The page also previews the C++29 direction: `[[profiles::enforce(bounds, type, lifetime)]]` (P3081/P3589/P3984) collapses runtime-checkable analyzer rules into compiler enforcement; P3294 token injection auto-generates the qualification-kit-required boilerplate (audit trails, traceability tags) at the declaration site.

https://wrocpp.github.io/toolset/qualified-compilers/

## Hashtags
#cpp #cpp26 #iso26262 #iec61508 #do178c #iec62304 #misra #autosar #functionalsafety #qualifiedcompiler #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Qualified C++ compilers in 2026". Subhead: vendor matrix across ISO 26262 / IEC 61508 / DO-178C / IEC 62304 + reflection-driven MISRA lint that shrinks the qualification surface. Citation: wro.cpp 2026-05-28.

## Suggested post time
Thursday 2026-05-28, 10:00 CET
Reason: Mid-week morning slot reaches EU automotive + industrial + avionics engineers in flow. Toolset launch fits the off-day cadence between reflection-series posts.
