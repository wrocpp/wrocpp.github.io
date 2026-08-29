# The bug got an answer in 95 minutes

## Body
In August this site wrote up a GCC and clang disagreement: a C++26 structured binding used as an if condition, over a tuple protocol type, rejected by GCC in a constant expression and accepted by clang.

That post noted the tracker had no report. On 27 August it got one.

Filed 15:44 UTC. Reduced testcase from Jakub Jelinek at 16:42. Root cause at 17:19, ninety five minutes after filing, from the person who implemented the feature in the first place.

The cause is neater than a missing case. Building the condition holds the conversion to bool in a temporary. A cleanup point then wraps the whole declaration to destroy temporaries, as CWG 2867 requires, and it covers that bool too.

At run time nothing shows, because a bool has no destructor. Constant evaluation tracks lifetime exactly, so reading it is an error.

https://wrocpp.github.io/posts/p0963-bug-root-caused/

## Hashtags
#cpp #cplusplus #gcc #cpp26 #compilers

## Alt-text
A wro.cpp social card reading "Filed at 15:44, root caused by 17:19", about a GCC bug diagnosed the same afternoon.

## Suggested post time
Friday 2026-10-30, 09:00 CET
Reason: Weekday morning for a compiler internals read.
