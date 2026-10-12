# A moved-from std::function can still hold the callable

## Body
After std::function f2 = std::move(f), the source f is empty on libstdc++ and still holds the callable on libc++, as long as the callable is small. A lambda that captures one shared_ptr is small.

QTBUG-151347, filed on 2026-10-12 against the Qt HarmonyOS plugin, comes from that difference. The plugin queues tasks to another thread and assumes each move empties the source. The leftover copy is destroyed on the sending thread, possibly as the last reference to the captured state.

The post has a demo that prints which thread drops the last reference. On clang trunk with libc++ it prints PRODUCER, on GCC 16.1 it prints WORKER. It also covers the standard wording, the libc++ move constructor, and why std::move_only_function is not available on libc++ yet.

https://wrocpp.github.io/posts/moved-from-function/

## Hashtags
#cpp #cplusplus #libcxx #concurrency #qt #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "On libc++, std::move leaves the callable behind" with a subtitle saying a small callable stays in the moved-from std::function and libstdc++ empties it. Citation footer: wro.cpp, 2026-10-13.

## Suggested post time
Tuesday 2026-10-13, 16:00 UTC
Reason: second post of the day; the function_ref post holds the 08:00 UTC slot.
