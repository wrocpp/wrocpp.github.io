# C++ Safety State of the Union: December 2026

## Body
Two libstdc++ CVEs from October and November have fixes on the GCC 16 release branch, and GCC 16.2, the newest release, has neither.

CVE-2026-125709: a single-character file stream write that fails still appends to the buffer, and repeated failures write past its end. Red Hat rates it 4.2. CVE-2026-115455: reading a bitset from a wide stream overflows the stack. Red Hat rates it 6.5 and added RHEL errata for it on 11 and 12 November.

The rest of the roundup, each item with its source:
- Contracts stay in the C++26 draft. A second ballot is planned, eight weeks long per Mateusz Pusz, with no start date.
- No outcome for profiles or SG23 was reported from Buzios.
- On Compiler Explorer, GCC 16.2 printed 0 for an unset int in C++26 mode. Clang 22.1 printed the stale 12345 in both modes, and 0 with -ftrivial-auto-var-init=zero.
- The EU CRA date of 11 December 2026 binds Member States. Full application for manufacturers is 11 December 2027.
- MISRA C++:2023 TC1:2026 adds no guidelines, but checker reports may shift.

It ends with a 10-line checklist for this week, each line linked to the post that ran it.

https://wrocpp.github.io/posts/cpp-safety-state-of-the-union-december-2026/

## Hashtags
#cpp #cpp26 #safety #security #libstdcxx #CRA #MISRA #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Two libstdc++ CVEs, fixed in no GCC release" with a subtitle about the GCC 16 branch, contracts in the C++26 draft, profiles and a 10-line checklist. Citation footer: wro.cpp, 2026-12-07.

## Suggested post time
Monday 2026-12-07, 16:00 UTC
Reason: the second slot of the day, beside the 08:00 UTC tidy-agent episode.
