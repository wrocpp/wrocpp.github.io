# The bug got an answer in 95 minutes

## Body
In August this site wrote up a disagreement between GCC and clang. A C++26 structured binding used as an if condition, over a type that decomposes through the tuple protocol, is rejected by GCC when the call happens in a constant expression. Clang accepts it. Remove any one of the three ingredients and GCC accepts it too.

That post ended by noting the tracker had no report covering it. On 27 August it got one. What happened next is the part worth writing down.

The report went in at 15:44 UTC. At 16:42 Jakub Jelinek posted a reduced testcase. At 17:19, ninety five minutes after filing, he posted the root cause with the compiler internals quoted. Jelinek implemented P0963 in GCC, so the person who wrote the feature read the report and diagnosed it before the end of the day.

His reduction drops every header. std::size_t becomes decltype(sizeof 0), tuple_size and tuple_element are forward declared rather than included, and the specialisation uses a plain static constexpr int instead of integral_constant. He also built it on the form where get returns a reference, which keeps the property that the failure does not depend on temporaries.

The cause is neater than a missing case. For a tuple protocol type the standard requires the contextual conversion to bool to happen before the get calls, so GCC evaluates it and holds the result in a temporary. Then a cleanup point wraps the whole declaration, and that cleanup point exists to destroy temporaries created while initialising a structured binding, as CWG 2867 requires. It also covers the bool holding the condition.

At run time nothing shows: a bool has no destructor and the storage still holds the value. Constant evaluation tracks lifetime exactly, so reading it is an error rather than a value.

A fix for one core issue reaching one object too far, and only the strictest mode in the compiler is exacting enough to see it.

https://wrocpp.github.io/posts/p0963-bug-root-caused/

What is the fastest a bug report of yours has ever been answered?

## Hashtags
#cpp #cplusplus #gcc #cpp26 #compilers

## Alt-text
A wro.cpp social card reading "Filed at 15:44, root caused by 17:19", about a GCC bug diagnosed the same afternoon.

## Suggested post time
Friday 2026-10-30, 09:00 CET
Reason: Weekday morning for a compiler internals read.
