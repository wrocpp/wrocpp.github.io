# A vector<bool> of SIZE_MAX bits builds on GCC 16.2 and throws on trunk

## Body
On GCC 16.2, a std::vector<bool> built from one of the 63 largest size_t values constructs without an error. Its size() equals the request and its capacity() is 0. A GCC trunk build of 6 November throws std::length_error on the same line.

The cause is the word count, (n + 63) / 64, which wraps to zero near SIZE_MAX. The fix is libstdc++ commit 2fd8866591, tracked as CVE-2026-114691. It is on the GCC 14, 15 and 16 branches, and as of 6 November no point release contains it.

Nothing fails at construction. Reading element 0 printed 0 in plain, UBSan, assertions and hardened builds. Only AddressSanitizer reported it. The practice is to check an untrusted count against max_size() before the constructor, and to rebuild against fixed headers.

https://wrocpp.github.io/posts/vector-bool-size-wraps-to-zero/

## Hashtags
#cpp #gcc #libstdcpp #security #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A bool vector with no storage claims SIZE_MAX bits" with a subtitle about GCC 16.2, trunk and the missing point release. Citation footer: wro.cpp, 2026-11-09.

## Suggested post time
Monday 2026-11-09, 16:00 UTC
Reason: the second slot of the day, while the fix is on the branches but in no release.
