# Three scope guards, and the one that is allowed to throw

## Body
Library Fundamentals defines three scope guards. scope_exit and scope_fail have noexcept destructors, so a throwing action there calls std::terminate. scope_success runs only on a normal exit, so its action may throw, which suits a commit that can fail. For a guard holding a throwing action, GCC 16.2 reports the three destructors as noexcept 1, 1 and 0.

https://wrocpp.github.io/posts/raii-scope-guards/

## Hashtags
#cpp #raii #exceptions #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "The one scope guard that is allowed to throw" with a subtitle about scope_exit, scope_fail and scope_success on GCC 16.2. Citation footer: wro.cpp, 2026-12-12.

## Suggested post time
Saturday 2026-12-12, 08:00 UTC
Reason: the morning slot on publication day; the next post, on FFmpeg, builds on this one.
