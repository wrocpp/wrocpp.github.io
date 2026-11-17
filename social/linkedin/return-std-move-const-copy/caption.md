# Moving a const object returns a copy: 163 page faults per call on a 400 KB vector

## Body
return std::move(book) on a const local is a copy.

std::move on a const object yields a const T&&, and only the copy constructor accepts that. I measured it on GCC 16.2 with a 400 KB std::vector<double>: the const case took 163 minor page faults per call (162.87 to 163.00), where a plain return and a moved non-const vector took 0 to 0.39. The time per call ran from 198 to 1354 microseconds on a shared machine, so I trust the fault count more.

GCC 16.2 and Clang 22.1 warn on the const local with -Wall -Wextra, with the same text they print for a harmless move. Neither warns on a const member moved inside a const function, or on a const local used in an initialisation. clang-tidy performance-move-const-arg flagged both. The post lists seven shapes and which tool reports each.

The faults depend on glibc's malloc thresholds: raising both mmap and trim thresholds with mallopt removed them. For a string in a struct, passing by value allocates from 16 characters on libstdc++ and costs none below that. A parameter the function stores is where by value plus std::move is right.

This builds on an advert for a paid C++ trading course that Henrique Bucher posted. I have not seen the course or its measurements, so everything above comes from programs of my own. I did not test printf, unordered_map, Clang 18 or any trading workload.

https://wrocpp.github.io/posts/return-std-move-const-copy/

## Hashtags
#cpp #cpp26 #movesemantics #copyelision #performance #clangtidy #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Move a const local and you copy 400 KB" with a subtitle about 163 page faults per call on GCC 16.2 and the shapes that clang-tidy flags. Citation footer: wro.cpp, 2026-12-28.

## Suggested post time
Monday 2026-12-28, 08:00 UTC
Reason: the morning slot on the publication day, last of the seven daily posts from 22 December.
