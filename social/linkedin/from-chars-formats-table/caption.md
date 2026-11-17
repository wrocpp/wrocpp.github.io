# std::from_chars rejects a leading plus, and hex reads 1e3 as 483

## Body
The string 1e3 has three different answers in std::from_chars, depending on the format you pass.

I ran 14 inputs through the four chars_format values on GCC 16.2 and on clang 22.1 with libstdc++ and with libc++. Of the 56 results, 34 succeed, 15 are invalid and 7 are out of range.

General format reads 1e3 as 1000. Fixed format stops at the exponent, consumes one character and returns 1, with no error. Hex format reads 1e3 as the hexadecimal number 483. A leading plus and a leading space fail in all four formats, while strtod accepts both.

libstdc++ and libc++ agree on every consumed count and every error code. They differ in one value: after an out-of-range result libstdc++ leaves the variable alone, and libc++ writes infinity or 0, although the standard says it stays unmodified.

The example checks all 56 results against a table and exits 0 only when they match. I also read how the two libraries parse: libstdc++ 16 calls fast_float, and libc++ uses LLVM libc code. Daniel Lemire's proposed fast_float hints are a separate pull request, open on 2026-11-17, and std::from_chars takes none of them.

https://wrocpp.github.io/posts/from-chars-formats-table/

## Hashtags
#cpp #cpp17 #charconv #fromchars #parsing #floatingpoint #libstdcpp #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "from_chars reads 1e3 as 1000, 1 or 483" with a subtitle about the four chars_format values, the leading plus and the libstdc++ and libc++ difference. Citation footer: wro.cpp, 2026-12-20.

## Suggested post time
Sunday 2026-12-20, 08:00 UTC
Reason: the morning slot on the publication day.
