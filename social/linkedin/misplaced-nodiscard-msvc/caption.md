# MSVC ignores a [[nodiscard]] written after static, and /W4 says nothing

## Body
Write static [[nodiscard]] int f() and MSVC compiles it at warning level 4 without a word.

Giovanni Dicanio hit this on Visual Studio 2022. The attribute is dropped, so a call that throws the result away is not reported either. I ran the form on four MSVC builds on Compiler Explorer, 19.30 to 19.51, and all four stayed silent at /W4. A reader, Jiri Havel, listed eight keywords that do the same (static, inline, constexpr, virtual, friend, explicit, __forceinline, __declspec). All eight behave that way in my runs.

GCC 16.2 and Clang reject the misplaced form. The one exception is an explicit constructor, which GCC only warns about.

MSVC has a warning for it, C5240, but it is off at /W4. Adding /we5240 makes every one of the nine test declarations an error, on 19.30 and on 19.51. Writing the attribute first, [[nodiscard]] static int f(), gives the expected C4834 on a discarded call.

The post has the full compiler table, the quoted messages and a grep pattern that finds the misplaced form.

https://wrocpp.github.io/posts/misplaced-nodiscard-msvc/

## Hashtags
#cpp #msvc #visualstudio #nodiscard #compilerwarnings #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One keyword turns [[nodiscard]] off on MSVC" with a subtitle saying static [[nodiscard]] compiles silently at /W4, GCC and Clang reject it, and /we5240 makes it an error. Citation footer: wro.cpp, 2026-12-02.

## Suggested post time
Wednesday 2026-12-02, 16:00 UTC
Reason: the second slot of the day, beside the 08:00 UTC tidy-agent series post.
