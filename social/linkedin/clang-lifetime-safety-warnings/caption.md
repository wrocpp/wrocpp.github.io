# Clang 23.1 -Wlifetime-safety warns on 6 of 7 dangling cases, GCC 16.2 on 1

## Body
I compiled seven small programs that dangle with Clang 23.1, Clang trunk and GCC 16.2 on 2026-11-17.

With -Wlifetime-safety, Clang 23.1 warned on six: a string_view returned from a local, a string_view returned from a parameter, a lambda capture that escapes, a reference held across push_back, a string_view of a temporary, and a string_view field set from a parameter. GCC 16.2 with -Wall -Wextra -Wdangling-pointer=2 -Wdangling-reference gave one correct report, on a reference field bound to a temporary, and it points inside basic_string.h.

Half of that lead is not new. Without the flag, Clang 23.1 already warned on three of the cases. The flag adds the lambda capture, the push_back reference and the view field. On Clang trunk the push_back check moved to -Wlifetime-safety-experimental-invalidation, so the 23.1 flags lose it there. Clang also flagged one correct program, where reserve leaves room for the push_back.

AddressSanitizer reported heap-use-after-free on two of the cases, with GCC and with Clang. The post lists the flags I would add to a Clang CI job and quotes every warning.

https://wrocpp.github.io/posts/clang-lifetime-safety-warnings/

## Hashtags
#cpp #cpp26 #clang #gcc #lifetime #safety #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Clang 23.1 warns on 6 of 7 dangling cases" with a subtitle about -Wlifetime-safety and GCC 16.2. Citation footer: wro.cpp, 2026-11-23.

## Suggested post time
Monday 2026-11-23, 08:00 UTC
Reason: the morning slot on the publication day.
