# Is std::vector consteval or constexpr?

## Body
A reader asked us in Slack: "Is std::vector consteval and not constexpr?"

Short answer: no. std::vector is constexpr-friendly since C++20. But the intuition behind the question is right -- vector values can only exist during constant evaluation, never as namespace-scope variables. Today's post unpacks the constexpr / consteval / constinit trio, the transient-allocation rule that gates everything, and the std::define_static_array (P3491) "promote" step that turns a one-shot consteval value into static-storage data your runtime program can iterate.

Runnable godbolt with a one-line toggle between the two specifiers included.

https://wrocpp.github.io/posts/vector-consteval-or-constexpr/

## Hashtags
#cpp #cpp26 #reflection #constexpr #consteval #wrocpp #cpp26reflection #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Is std::vector consteval, or constexpr?" Subhead: short answer is constexpr since C++20; the intuition that vector "is consteval" is operationally right because its values only exist during constant evaluation. Citation: wro.cpp 2026-05-12.

## Suggested post time
Tuesday 2026-05-12, 10:00 CET
Reason: matches the reflection-series cadence (Buffer fires at 08:00 UTC). Tuesday 10am hits EU C++ engineers post-standup.
