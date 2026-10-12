# A moved-from std::function can still hold the callable

## Body
On libc++, a std::function that you moved from can still hold a small callable. On libstdc++ it is empty. A Qt HarmonyOS bug filed on 2026-10-12 shows the cost: a task queued to another thread was destroyed on the thread that sent it.

The post has a demo that prints the destroying thread on both libraries.

https://wrocpp.github.io/posts/moved-from-function/

## Hashtags
#cpp #cplusplus #libcxx #concurrency #qt #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "On libc++, std::move leaves the callable behind" with a subtitle saying a small callable stays in the moved-from std::function and libstdc++ empties it. Citation footer: wro.cpp, 2026-10-13.

## Suggested post time
Tuesday 2026-10-13, 16:00 UTC
Reason: second post of the day; the function_ref post holds the 08:00 UTC slot.
