# The May 2026 WG21 mailing in five papers (pre-Brno, 116 total)

## Body
WG21's pre-Brno mailing landed in early May (**116 papers**, the largest pre-meeting volume since the C++20 design crunch). Brno meets 8-13 June. Five papers are doing the heavy lifting for the threads worth tracking:

**1. P2000R0 - Direction for ISO C++29** (Vandevoorde, Garland, McKenney, Orr, Stroustrup, Wong). The formal direction-setting paper for C++29. **Safety is named as the headline axis**. The committee adopted the line "C++29 must deliver on the safety story C++26 began but did not finish." Retroactively justifies the "deferred to C++29" framing on every memory-safety toolset page.

**2. D3704R0 - A type-safety profile** (Stroustrup). The next iteration past the C++26 deferral, re-aligned on top of Dos Reis's P3589 general framework, addressing the Bloomberg P3543 counter-paper critiques head-on: per-rule granularity, structured error reporting, explicit migration paths. **SG23 focus at Brno.**

**3. P3970R0 - Profiles and Safety: a call to action** (same co-author group as P2000). 8 pages; the argument: committee owes the community concrete profile timelines, not just direction prose. Names three milestones (SG23 framework R1 at Brno, type-safety profile R1 by autumn, vote at November). Signal that the C++29 deliverable isn't slipping further.

**4. P4003R0 - Coroutines for I/O** (Liard, Baker, Voržáček). **First LEWG review at Brno.** The standard-library complement to `std::execution`: a coroutine-aware I/O model that composes with C++26 senders/receivers. Doesn't promise C++29; doesn't promise to look exactly like libunifex; does promise to stop reinventing socket-loop integration for every reactor library in the ecosystem. If you've hand-rolled an async-I/O coroutine wrapper for boost::asio or liburing, this is the target.

**5. P3294 - Token sequence injection** (Revzin, Alexandrescu, Vandevoorde). Re-revised for the May mailing with refined ergonomics. No shipping compiler implements it yet; clang-p2996 has the closest substrate. Cross-link: Revzin's C++Now keynote earlier this month is the design-space tour these papers live inside.

Honourable mentions: std::execution ratification follow-ups, pattern matching (P1371) revisions, linalg maintenance, reflection edge-case papers, modules ergonomics. Full list at open-std.org/jtc1/sc22/wg21/docs/papers/2026/.

Sutter's Brno trip report typically posts within 48 hours of meeting close; wro.cpp will run a Brno trip-report news short in the week of 15 June.

If you ship C++ and haven't taken the 2026 Developer Survey "Lite" on isocpp.org yet: 10 minutes, the standards committee + major tool vendors all read it directly.

https://wrocpp.github.io/posts/may-2026-wg21-mailing/

## Hashtags
#cpp #cpp26 #cpp29 #wg21 #brno #profiles #coroutines #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "May 2026 WG21 mailing in five papers". Subhead: Pre-Brno (8-13 June); 116 papers; safety direction (P2000+D3704+P3970), coroutines-for-I/O P4003, token injection P3294. Citation: wro.cpp 2026-05-27.

## Suggested post time
Wednesday 2026-05-27, 10:00 CET
Reason: Wednesday morning EU C++ audience; news short between Tue's tiny-orm and Thu's qualified-compilers launch.
