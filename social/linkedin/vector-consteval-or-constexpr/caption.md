# Is std::vector consteval or constexpr?

## Body
A reader asked me this in Slack right after our "template for" post shipped:

> Is std::vector consteval and not constexpr?

Short answer: no. Long answer: the intuition is right, the wording isn't, and the difference is exactly what std::define_static_array exists to bridge.

std::vector has been constexpr-friendly since C++20 -- you can sort one in a consteval function, return one, push_back inside a constant expression. But you cannot declare "constexpr std::vector<int> v" or "constinit std::vector<int> v" at namespace scope, because the heap allocation would have to escape transient constant evaluation. The container's storage is a one-shot deal: alive during the evaluation, gone at the end.

Today's post unpacks the constexpr / consteval / constinit trio, the transient-allocation rule, and three patterns for consuming a constant-time std::vector once you have one. Includes a runnable godbolt that toggles between constexpr and consteval with a single uncomment, plus an honest note on why SFINAE cannot discriminate the two specifiers in clang-p2996 today (and which P3795 reflection predicate fixes that once it ships).

If you are walking through the C++26 reflection series and have ever stared at "std::define_static_array(...)" wondering why the wrapper is needed -- this post is the answer.

https://wrocpp.github.io/posts/vector-consteval-or-constexpr/

## Hashtags
#cpp #cpp26 #reflection #constexpr #consteval #wrocpp #cpp26reflection #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Is std::vector consteval, or constexpr?" Subhead: short answer is constexpr since C++20; the intuition that vector "is consteval" is operationally right because its values only exist during constant evaluation. Citation: wro.cpp 2026-05-12.

## Suggested post time
Tuesday 2026-05-12, 10:00 CET
Reason: matches the reflection-series cadence (Buffer fires at 08:00 UTC = 10:00 CEST). Tuesday 10am hits EU C++ engineers post-standup; LinkedIn EMEA technical engagement peaks here.
