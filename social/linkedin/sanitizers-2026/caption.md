# Sanitizers in 2026 -- safety today, reflection tomorrow

## Body
The most concentrated source of memory-safety CVEs in real C++ codebases isn't index-out-of-bounds; it's **handwritten parsers at trust boundaries**. Every field read needs a bounds check; every offset needs to advance correctly; every type needs to match the wire format. Miss any of those once and you've shipped the next CVE.

The first wro.cpp Toolset launch under the new triptych structure (Today / Reflection today / Where this is heading) walks the safety story end-to-end:

TODAY -- ASan / UBSan / TSan / MSan / HWASan flag table, when-to-use-which guidance, three live demos via the wro.cpp cpp-safety container (use-after-free, signed-overflow, data-race), the CMake recipe, and the prerequisite that almost everyone forgets: sanitizers fire only on code that runs. Add example-based tests, property-based tests with RapidCheck, coverage-guided fuzzing with libFuzzer.

REFLECTION TODAY -- a reflection-driven binary parser at trust boundary, generated from the struct definition itself. C++26 reflection (clang-p2996, GCC 16.1) eliminates the actual CVE class -- not the textbook patterns sanitizers catch but the silent off-by-one in a custom parser nobody fuzzed. Aligned with Core Guidelines F.24 / F.43 / ES.42, MISRA C++, AUTOSAR C++14, and SEI CERT C++. Runnable godbolt link.

WHERE THIS IS HEADING -- C++26 profiles (P3081 Sutter, P3274 Stroustrup) make raw pointer arithmetic refuse to compile under [[profiles::enforce(bounds, type, lifetime)]]. C++29 token injection (P3294 Revzin / Alexandrescu / Vandevoorde) generates the safe parsers from a single schema annotation. The trust-boundary CVE class becomes a missing-annotation lint, not a runtime exploit.

Page lives forever; this is the launch.

https://wrocpp.github.io/toolset/sanitizers-2026/

## Hashtags
#cpp #cpp26 #safety #sanitizers #asan #reflection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Sanitizers in 2026". Subhead: ASan / UBSan / TSan today + reflection-driven safe parsers + the C++26 profiles + C++29 injection that makes most sanitizer-found bugs uncompilable. Citation: wro.cpp 2026-05-08.

## Suggested post time
Friday 2026-05-08, 10:00 CET
Reason: Friday morning hits EU C++ engineers wrapping the week + planning weekend reading. First wro.cpp Toolset launch in the Modern-C++-for-production expansion; positions the post for high engagement on the immediate launch + Saturday read-throughs.
