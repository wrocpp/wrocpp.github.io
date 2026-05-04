# Testing for safety in 2026 -- the four coverage levels and the reflection-driven shortcut

## Body
A test that writes `42` to a field and reads it back tests C++ assignment, not the production code. Real-world bugs are different shapes: parsers and serializers drift apart after one of them gains a field; an interface gains a method but only half its mocks know; the diagnostic on a failed assertion says "T != T" and you reach for a debugger.

C++26 reflection is the right shape for the bugs that follow mechanically from struct layout. Two patterns where reflection-alone genuinely earns its keep:

**arbitrary&lt;T&gt;** -- the C++ analogue of Rust's `#[derive(Arbitrary)]` and Haskell QuickCheck's `Generic` instances. Generic typed input generator. Production type stays clean; test code specialises `template <> struct TestSpec<T>` (mirroring std::hash / std::formatter), keyed by member-pointer NTTPs (`&T::field`), so renaming a production field breaks the spec at build time. The kernel walks the spec, returns the cross-product of per-field samples. Round-trip property test, fuzz harness, fixture factory, differential tests are short layers on top.

**pretty_diff** -- structural failure diagnostics. ~30 lines of library, walks any T at compile time, emits `field K: A != B` on assertion failure instead of the unreadable `T != T`. Replaces the hand-maintained dump.hpp every codebase grows and forgets to update.

Today's wro.cpp Toolset launch (MR4.5 in the safety cluster) covers all of it -- the four-level coverage ladder (Catch2/doctest/GoogleTest -> RapidCheck -> libFuzzer/AFL++ -> differential), the reflection patterns above with proper layering (production stays clean, test concerns in test code), and the C++29 token-injection direction (P3294) that finally makes mock synthesis competitive with GoogleMock.

What reflection-alone is NOT for: GoogleMock-style behavior mocks. Honest framing in the post -- the page says outright that argument matchers, sequenced expectations, and action wiring stay better in those frameworks until C++29 injection lands.

Cross-linked with sanitizers-2026 (the runtime safety net these tests feed) and memory-safety-cpp26-and-beyond (compile-time enforcement story).

https://wrocpp.github.io/toolset/testing-for-safety-2026/

## Hashtags
#cpp #cpp26 #reflection #testing #propertybased #fuzzing #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Testing for safety in 2026". Subhead: Catch2 / RapidCheck / libFuzzer / differential coverage ladder + reflection-driven arbitrary<T> kernel + structural pretty_diff. Citation: wro.cpp 2026-05-16.

## Suggested post time
Saturday 2026-05-16, 10:00 CET
Reason: Saturday morning catches weekend reading-list builders. MR4.5 toolset launch in the safety cluster; pairs with MR4 (Thu 5/14 memory-safety-cpp26-and-beyond) for the full safety triptych.
