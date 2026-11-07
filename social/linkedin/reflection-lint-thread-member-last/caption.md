# A reflection check that the thread member goes last

## Body
No compiler checks the rule that a std::jthread member is declared last. About 25 lines of C++26 reflection turn it into a static_assert for each class.

On GCC 16.2 and trunk the failing build prints a message we wrote: thread member 'worker' is declared before 'ticks'; declare the thread last. GCC 16.2 with -Wall -Wextra -Weffc++ said nothing about either order.

The check sees declaration order only, which is the rule and not the bug, so a thread that reads nothing is flagged too. It also misses a thread inside another type, a thread in a base class, and a vector of threads. The post tabulates each case I ran.

https://wrocpp.github.io/posts/reflection-lint-thread-member-last/

## Hashtags
#cpp #cpp26 #reflection #jthread #threads #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Thread member last, checked at compile time" with a subtitle about the 25-line reflection check and its limits. Citation footer: wro.cpp, 2026-12-18.

## Suggested post time
Friday 2026-12-18, 08:00 UTC
Reason: the morning slot, a follow-up to the 11 November thread member post.
