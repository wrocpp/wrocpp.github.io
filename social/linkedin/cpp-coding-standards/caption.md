# C++ coding standards in 2026: MISRA / SEI CERT / JSF AV side by side, plus the reflection-driven composable rule bundle

## Body
A regulated C++ project picks a coding standard. **MISRA C++:2023** for automotive (ISO 26262). **SEI CERT C++** for avionics + defense defensive coding. **JSF AV C++** for older fixed-wing avionics (DO-178C). Pick one, run the matching clang-tidy check set in CI, maintain an exception log. Then someone says "we also need to satisfy CERT for the audit cycle" and the analyzer-config matrix appears -- two checker passes, two suppression lists, two ways for them to disagree on the same line.

Quick disambiguation that catches a lot of teams: **MISRA C++:2023 superseded AUTOSAR C++14 in 2023**. Adaptive AUTOSAR cites MISRA directly. Many tool vendors still expose "AUTOSAR C++14" as a check-set name -- treat it as an alias and cite MISRA in new safety cases.

C++26 reflection makes the multi-standard problem composable. Encode each rule as a consteval predicate over `nonstatic_data_members_of(^^T)`; combine with `operator&&`:

```cpp
namespace standards {
template <typename T> consteval bool meets_misra_11_0_1();    // private members
template <typename T> consteval bool meets_cert_dcl56_cpp();  // no raw pointers
template <typename T> consteval bool meets_jsf_av_75();       // no bit-fields

template <typename T>
consteval bool all() {
    return meets_misra_11_0_1<T>() && meets_cert_dcl56_cpp<T>() && meets_jsf_av_75<T>();
}
}

class SensorReading { /* private members only */ };
static_assert(standards::all<SensorReading>());   // PASS
```

Add a public data member, MISRA fires; add a raw pointer field, CERT fires; add a bit-field, JSF fires. The diagnostic names the failing rule. **Multi-standard projects become a single static_assert.**

When NOT to use it: cross-TU analysis, statement-level rules (no `goto`, no recursion), style rules (clang-format), comment-mandate rules. The bundle complements analyzers; it does not replace them. The split is: bundle catches structural rules at compile time (cheap, immediate); analyzer catches the rest in CI (expensive, eventual). Multi-standard projects benefit most because the analyzer-config matrix shrinks.

The same `nonstatic_data_members_of` walker drives the hardened-stdlib lint, the qualified-compilers MISRA lint, the lifetime borrow lint, the SoA layout transform, the SBOM emit. One walker, six predicates, every rule orthogonal.

C++29 candidate features collapse the loop further: `[[profiles::enforce(misra_2023, cert_cpp)]] namespace sensor_fusion { ... }` would make the structural rules compiler-enforced subsets. P3294 token injection extends the pattern to inject standards-required boilerplate (audit headers, traceability tags) at the declaration site.

https://wrocpp.github.io/toolset/cpp-coding-standards/

## Hashtags
#cpp #cpp26 #misra #cert #jsf #autosar #functionalsafety #compliance #reflection #wrocpp #moderncpp #safety

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "C++ coding standards in 2026". Subhead: MISRA + CERT + JSF side by side; reflection-driven composable rule bundle that makes multi-standard projects a single static_assert. Citation: wro.cpp 2026-06-13.

## Suggested post time
Saturday 2026-06-13, 10:00 CET
Reason: Saturday morning EU automotive + avionics + defense audience; toolset launch fits the off-day cadence between reflection-series posts.
