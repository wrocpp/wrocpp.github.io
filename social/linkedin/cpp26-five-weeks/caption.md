# C++26 is done -- five weeks since Croydon, here's what shipped

## Body
Five weeks ago today WG21 voted C++26 to publication at the Croydon meeting outside London. The dust has settled enough to take stock.

The headline cluster is reflection. P2996 (the core facility) shipped together with P3394 (annotations), P3096 (function-parameter reflection), P3560 (the error-handling story), and P1306 (expansion statements). Same five-paper bundle the wro.cpp series teaches end-to-end.

P2900 contracts went in too, over Bjarne Stroustrup's well-publicised objection. P2300 senders/receivers landed after a decade of design iteration. The hardened libstdc++ profiles ship behind a single flag.

GCC 16.1 released on 30 April with `-freflection`. The Bloomberg clang-p2996 fork is still the bleeding edge. MSVC has it on the roadmap; EDG 6.6 has experimental support.

For the wro.cpp reflection series: posts 1-25 stay as-is. The audit auto-wired GCC 16.1 links to every example that compiles cleanly under stable reflection. Roughly 80 percent of the examples have a green GCC build today.

Five weeks from "the standard is done" to "your distro builds it" is the fastest C++ has ever moved from vote to running code. Worth marking the moment.

Read it: https://wrocpp.github.io/posts/cpp26-five-weeks/

What feature are you reaching for first?

## Hashtags
#cpp #cpp26 #p2996 #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline reads "C++26 is done." with the plus signs in orange and a blue period. Subtitle: five weeks since the Croydon vote, with reflection, contracts, senders/receivers, and hardened libstdc++ as the headline features that landed.

## Suggested post time
Saturday 2026-05-02, 10:00 CET
Reason: matches the post's pubDate so the link is live the morning the social card lands; Saturday morning is a quiet C++ news slot, which favours a recap-style post that wants reading time rather than competing with weekday release announcements.
