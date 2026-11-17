# Three scope guards, and the one that is allowed to throw

## Body
Library Fundamentals (P0052) defines three RAII scope guards, and libstdc++ ships them in <experimental/scope>. GCC 16.2 has all three. scope_exit runs on every exit, scope_fail only when an exception is unwinding, and scope_success only on a normal exit.

The destructors differ. scope_exit and scope_fail can run during unwinding, where a second exception calls std::terminate, so their destructors are unconditionally noexcept. scope_success never runs during unwinding, so its destructor is conditionally noexcept and its action may throw. GCC 16.2 reports 1, 1 and 0 for a guard holding a throwing action.

That makes scope_success the place for a commit that can fail. Amit G. published a small header with the same three guards that requires every action to be noexcept, and it rejects such a commit at compile time. The README states the tradeoff plainly. Neither choice is wrong.

https://wrocpp.github.io/posts/raii-scope-guards/

## Hashtags
#cpp #raii #exceptions #noexcept #libraryfundamentals #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "The one scope guard that is allowed to throw" with a subtitle about scope_exit, scope_fail and scope_success on GCC 16.2. Citation footer: wro.cpp, 2026-12-12.

## Suggested post time
Saturday 2026-12-12, 08:00 UTC
Reason: the morning slot on publication day; the next post, on FFmpeg, builds on this one.
