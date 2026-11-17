# Moving a const object returns a copy: 163 page faults per call on a 400 KB vector

## Body
return std::move(book) on a const local is a copy.

std::move on a const object gives a const T&&, which only the copy constructor accepts. On GCC 16.2 a 400 KB const vector took 163 page faults per call, and a plain return took none.

GCC and Clang warn about the const local with the same text they use for a harmless move. clang-tidy also flags two shapes they miss. By value for a string in a struct costs an allocation from 16 characters on libstdc++.

All numbers come from programs of my own, run on Compiler Explorer. I have not seen the course advert that prompted this post.

https://wrocpp.github.io/posts/return-std-move-const-copy/

## Hashtags
#cpp #cpp26 #movesemantics #copyelision #performance #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Move a const local and you copy 400 KB" with a subtitle about 163 page faults per call on GCC 16.2. Citation footer: wro.cpp, 2026-12-28.

## Suggested post time
Monday 2026-12-28, 08:00 UTC
Reason: the morning slot on the publication day.
