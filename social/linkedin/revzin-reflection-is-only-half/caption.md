# Barry Revzin at C++Now: "Reflection Is Only Half the Story"

## Body
Barry Revzin keynoted **C++Now 2026** (Mon 4 May, Aspen) with the line C++26 reflection users have been circling for two years:

> *"C++26 gives us reflection, the culmination of decades of work building up support for more compile-time programming in C++. But reflection primarily only lets us OBSERVE. The important next question is: what might it look like if we were to GENERATE?"*

The talk is a 90-minute tour of source-code generation design space. Not a P3294 advocacy talk (Revzin co-authored it but explicitly presents alternatives); not a Rust-is-better talk; not a "C++29 will ship this" talk. It's a careful comparison of how Rust, Swift, and D do code-gen, what axes matter (capability / composability / cohesion / debuggability / ergonomics / error quality), and which of today's C++ mechanisms (macros, templates) hit which walls.

Why this matters for code you might be writing right now: every `meets_<rule><T>()` predicate in the wro.cpp toolset cluster (hardened-stdlib schema lint, MISRA Rule 11.0.1 check, lifetime borrow lint, CycloneDX SBOM emit) is **observation**. They walk `nonstatic_data_members_of` and refuse to compile or emit JSON. None of them generate new code alongside the observed type.

The cases where reflection-only hits a ceiling are exactly the ones marked "Where this is heading: C++29 token injection" on each toolset page. Reflection cannot synthesise a `MOCK_METHOD`-equivalent class alongside an interface, cannot emit a `safe_index_at()` accessor next to a raw `data[]` member, cannot inject `safe_format` annotation-driven boilerplate. Each is "make a NEW declaration based on what reflection sees": generation, not observation.

The video isn't out yet (C++Now typically posts keynotes ~3-4 weeks after; check around mid-June). Until then: conference page abstract covers the structure, attendees posted detailed notes on C++ Slack and /r/cpp within 24 hours, Revzin's own blog usually gets a slide-deck companion within a week.

Also worth a click from the same conference: Mark Hoemmen on multidimensional `std::execution` (relevant for the simd-in-cpp-2026 toolset entry) and Matt Godbolt on benchmarking (relevant for profiling-cpp-2026).

Pre-Brno context: WG21 reconvenes 8-13 June in Brno; the May 2026 mailing dropped early this month (116 papers). The 2026 C++ Developer Survey "Lite" is open through mid-May. If you ship C++, the 10-minute survey is the highest-leverage feedback channel into both the standards committee and the tool vendors.

https://wrocpp.github.io/posts/revzin-reflection-is-only-half/

## Hashtags
#cpp #cpp26 #cpp29 #reflection #codegen #cppnow #wrocpp #moderncpp #revzin

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Revzin: Reflection Is Only Half the Story". Subhead: C++Now 2026 keynote on what comes after observation -- the source-code-generation design space. Citation: wro.cpp 2026-05-23.

## Suggested post time
Saturday 2026-05-23, 10:00 CET
Reason: Saturday morning EU C++ audience; news short in the off-day slot between Fri's post 12 (clap-for-cpp) and Sun's MR6 hardened-stdlib launch.
