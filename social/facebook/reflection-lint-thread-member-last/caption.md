# A reflection check that the thread member goes last

## Body
About 25 lines of C++26 reflection turn "declare the std::jthread member last" into a static_assert per class. On GCC 16.2 and trunk the failing build names the thread and the member declared after it. The check sees declaration order only, so it also flags a thread that reads nothing.

https://wrocpp.github.io/posts/reflection-lint-thread-member-last/

## Hashtags
#cpp #cpp26 #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Thread member last, checked at compile time" with a subtitle about the 25-line reflection check and its limits. Citation footer: wro.cpp, 2026-12-18.

## Suggested post time
Friday 2026-12-18, 08:00 UTC
Reason: the morning slot, a follow-up to the 11 November thread member post.
