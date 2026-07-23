# The July 2026 C++ mailing, in five papers

## Body
The first WG21 mailing after the June Brno meeting is out, and it is a memory-safety document. Four of its papers are the same argument: what, exactly, is a safety profile.

Peter Bindels contributes three companion papers (P4314 to P4316) pinning down the mechanics the profiles proposal has left vague: how you activate a profile, what its specification must contain, and a reusable skeleton so each one is written the same way. Vinnie Falco proposes std::core_ub (P4317), a profile that inserts runtime checks for core-language undefined behavior that can be caught, turning silent UB into a defined trap. Bjarne Stroustrup's initialization profile reaches R2 (P4222), guaranteeing objects are used only after initialization.

Then the paper to read closely: Falco again, in P4318 "Transient Benefit, Perpetual Cost", arguing that baking implicit runtime assertions into the core language buys a short-term safety win at a permanent cost. The same author proposing a checking profile and arguing against implicit checks is the point. It is a careful argument about where checking belongs.

The wildcard is P4312 "Effect Sets" (Michael Galuszka), which generalizes noexcept into composable, tracked effect annotations. An early sketch, but the most interesting swing in the batch.

Full rundown, with the bitmask-enums and ranges-views papers linked: https://wrocpp.github.io/posts/wg21-2026-07-mailing/

Where do you land: runtime checks in the language, or kept in the library?

## Hashtags
#cpp #cplusplus #wg21 #cpp29 #memorysafety #standardization

## Alt-text
A cream wro.cpp social card reading "One author argues both sides of C++ safety", about the July 2026 WG21 mailing and the safety-profiles papers.

## Suggested post time
Saturday 2026-08-08, 10:00 CET
Reason: weekend mid-morning suits a longer committee-news read.
