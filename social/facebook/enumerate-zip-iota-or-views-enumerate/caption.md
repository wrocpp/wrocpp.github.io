# views::enumerate is sized and common, and zip(iota, r) is neither

## Body
A hand-written enumerate built as zip(iota, r), shown by Alex Dathskovsky, is not sized and not common on GCC 16.2 and libc++ trunk. Building a vector from it takes 2000 iterator steps over 1000 elements, and views::enumerate takes 1000. A bounded iota brings size and a common end back. libc++ 22.1 has no views::enumerate.

https://wrocpp.github.io/posts/enumerate-zip-iota-or-views-enumerate/

## Hashtags
#cpp #cpp23 #ranges #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A zip-based enumerate has no size and no common end" with a subtitle about 2000 iterator steps against 1000 for views::enumerate. Citation footer: wro.cpp, 2026-12-26.

## Suggested post time
Saturday 2026-12-26, 08:00 UTC
Reason: the morning slot on the publication day.
