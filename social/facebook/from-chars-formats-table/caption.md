# std::from_chars rejects a leading plus, and hex reads 1e3 as 483

## Body
The string 1e3 has three answers in std::from_chars, depending on the format. General gives 1000, fixed stops after the 1 and returns 1 with no error, and hex reads 483.

I ran 14 inputs through the four formats on GCC 16.2 and clang 22.1, with libstdc++ and libc++. A leading plus and a leading space fail in all four. The two libraries agree on every count and error code, and differ in the value left after an out-of-range result.

https://wrocpp.github.io/posts/from-chars-formats-table/

## Hashtags
#cpp #cpp17 #charconv #parsing #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "from_chars reads 1e3 as 1000, 1 or 483" with a subtitle about the four chars_format values. Citation footer: wro.cpp, 2026-12-20.

## Suggested post time
Sunday 2026-12-20, 08:00 UTC
Reason: the morning slot on the publication day.
