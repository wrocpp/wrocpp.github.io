# views::as_input before filter turns a reverse bug into an error

## Body
A filter, a reverse and as_rvalue over a vector of strings compile on GCC 16.2 and overflow the heap under AddressSanitizer. The case comes from P3725R3 by Nicolai Josuttis.

Put views::as_input before the filter and the same pipeline stops compiling at the reverse, because the filtered view is now input-only. The cost is that it is single pass. libstdc++ 15 calls the adaptor to_input, libstdc++ 16.2 calls it as_input, and libc++ trunk had neither on Compiler Explorer.

https://wrocpp.github.io/posts/views-as-input-before-filter/

## Hashtags
#cpp #cpp26 #ranges #views #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One adaptor turns a filter bug into a compile error" with a subtitle about filter, reverse and as_rvalue overflowing the heap on GCC 16.2 and views::as_input making the reverse a compile error. Citation footer: wro.cpp, 2026-11-26.

## Suggested post time
Thursday 2026-11-26, 08:00 UTC
Reason: the morning slot on the publication day.
