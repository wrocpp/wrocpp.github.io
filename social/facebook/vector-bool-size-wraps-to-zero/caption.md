# A vector<bool> of SIZE_MAX bits builds on GCC 16.2 and throws on trunk

## Body
On GCC 16.2, a std::vector<bool> built from a size near SIZE_MAX constructs without an error, reports that size and owns no storage. GCC trunk throws std::length_error. The fix is on the 14, 15 and 16 branches (CVE-2026-114691), and as of 6 November no point release has it. Only AddressSanitizer reports the bad read.

https://wrocpp.github.io/posts/vector-bool-size-wraps-to-zero/

## Hashtags
#cpp #gcc #security #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A bool vector with no storage claims SIZE_MAX bits" with a subtitle about GCC 16.2, trunk and the missing point release. Citation footer: wro.cpp, 2026-11-09.

## Suggested post time
Monday 2026-11-09, 16:00 UTC
Reason: the second slot of the day.
