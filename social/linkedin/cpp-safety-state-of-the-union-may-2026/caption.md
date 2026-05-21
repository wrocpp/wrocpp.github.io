# C++ Safety State of the Union: May 2026

## Body
C++ in May 2026 has four conversations running at once. None of them talks to the others in public. This essay wires them.

**The regulators** (CISA Jan 2026 deadline + EU CRA) want manufacturer memory-safety roadmaps. That deadline has passed. Stroustrup's framing was blunt: "credible threat", "unprecedented serious attacks", "we risk a painful decline."

**The committee** voted at Hagenberg: 19 profiles / 9 Safe C++ / 11 both. Profiles won the lane. C++26 shipped three pieces of the answer -- P2900 contracts, P3471 hardened stdlib, P2996 reflection. The headline -- `[[profiles::enforce]]` -- was deferred to C++29. P3970R0 "Profiles and Safety: a call to action" (Vandevoorde + Stroustrup + Garland + McKenney + Orr + Wong, Jan 2026) names three milestones to defend the new timeline.

**The industry** shipped first. Chromium: 70% of high-sev bugs are memory bugs; MiraclePtr cut UAF by 57%. Android: > 60% high-sev is memory; MTE production on Pixel. Apple's libc++ safe-buffers landed via LLVM RFC -- Chandler Carruth credits Apple with the ecosystem-wide tipping point. P3471 deployment data: 0.3% perf cost across hundreds of millions of LOC, 1000+ bugs found.

**What to do today** is the five things that compose into a safety baseline regardless of what C++29 ships: flip the hardened-stdlib macro, wire ASan+UBSan in CI, enable lifetime warnings + scope guards, author contracts at module boundaries, define the testing matrix (example / property / fuzz / differential).

The companion piece is the new wro.cpp toolset reading list -- 30+ curated sources across committee papers, talks, deployment reports, blog posts, and regulatory references. Quarterly refresh. Implementation-grade sources only -- no hot-take aggregators.

Pre-Brno (8-13 June 2026) reading. The wro.cpp angle: cor3ntin's "Legacy Safety: The Wroclaw C++ Meeting" post made Wroclaw the unofficial venue for the legacy-safety conversation. This is our continuation.

https://wrocpp.github.io/posts/cpp-safety-state-of-the-union-may-2026/

## Hashtags
#cpp #cpp26 #cpp29 #safety #security #profiles #contracts #hardenedstdlib #cisa #wg21 #brno #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "C++ Safety State of the Union: May 2026". Subhead: Regulators, committee, industry, and the five things to wire today -- wired into one essay + a quarterly-refreshed reading list. Citation: wro.cpp 2026-05-25.

## Suggested post time
Monday 2026-05-25, 10:00 CET
Reason: Monday morning slot for EU C++ + decision-maker audience opening their week with a state-of-the-union read. Pre-Brno (8-13 June) framing makes the timing load-bearing.
