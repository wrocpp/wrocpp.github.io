# MSVC ignores a [[nodiscard]] written after static, and /W4 says nothing

## Body
static [[nodiscard]] int f() compiles on MSVC at /W4 with no diagnostic, and a discarded call goes unreported. Four MSVC builds on Compiler Explorer, 19.30 to 19.51, did this for all eight keywords a reader listed. GCC and Clang reject the form. Put the attribute first, and add /we5240 to make the misplaced form an error.

https://wrocpp.github.io/posts/misplaced-nodiscard-msvc/

## Hashtags
#cpp #msvc #nodiscard #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One keyword turns [[nodiscard]] off on MSVC" with a subtitle saying static [[nodiscard]] compiles silently at /W4, GCC and Clang reject it, and /we5240 makes it an error. Citation footer: wro.cpp, 2026-12-02.

## Suggested post time
Wednesday 2026-12-02, 16:00 UTC
Reason: the second slot of the day, beside the 08:00 UTC tidy-agent series post.
