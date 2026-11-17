# views::enumerate is sized and common, and zip(iota, r) is neither

## Body
Alex Dathskovsky showed a C++23 enumerate adaptor built as zip(iota, r) in a range_adaptor_closure. It is a clean example of that class, and this post asks what std::views::enumerate does differently.

On GCC 16.2 and libc++ trunk, the zip version over a vector<int> is not a sized_range and not a common_range, and views::enumerate is both. So size() does not compile on it, and neither does the iterator-pair vector constructor. ranges::to<vector> allocates once for both, but takes 2000 iterator steps over 1000 elements against 1000 for views::enumerate. Bounding the iota by the size of the range brings back size, a common end and a signed index.

libc++ 22.1 has no views::enumerate, and libc++ trunk has it. I did not run MSVC, input-only ranges or wall-clock time.

https://wrocpp.github.io/posts/enumerate-zip-iota-or-views-enumerate/

## Hashtags
#cpp #cpp23 #ranges #zip #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A zip-based enumerate has no size and no common end" with a subtitle about 2000 iterator steps against 1000 for views::enumerate. Citation footer: wro.cpp, 2026-12-26.

## Suggested post time
Saturday 2026-12-26, 08:00 UTC
Reason: the morning slot on the publication day.
