# Fertig: this is not the cast you're looking for

## Body
Andreas Fertig's post **"What reinterpret_cast doesn't do"** (re-shared on isocpp.org Mon 2026-05-18) opens with the line C++ teachers have been waiting two decades to say cleanly: "This is not the cast you're looking for."

The punchline: `reinterpret_cast` and C++23's `std::start_lifetime_as` look interchangeable, but only if you don't read the abstract-machine fine print.

`reinterpret_cast<T*>(p)` re-interprets a bit pattern as a pointer of a different type. That's a **pointer operation**, not an object-lifetime operation. The compiler still believes whatever object was at that address is whatever it was before. Accessing the new type through the `reinterpret_cast`-derived pointer is undefined behaviour under strict aliasing for nearly every non-pointer-character type pair. It "works" because compilers tolerate the pattern most of the time, until they don't, usually on a release build, on a customer's machine, after an unrelated optimisation pass.

C++23's `std::start_lifetime_as<T>(ptr)` returns a `T*` AND tells the abstract machine "an object of type T now begins its lifetime at this address." That second half is precisely what `reinterpret_cast` cannot do.

Where this matters in production C++:
- Binary protocol parsers (read N bytes into a buffer, start_lifetime_as as a `Header`)
- Embedded MMIO (Fertig's training-class motivation)
- Shared-memory IPC (consumer needs to treat the segment as the struct without re-running the constructor)
- Custom allocators populating raw storage before the pointer goes out

Five-line difference between UB-then-it-works-on-my-compiler and defined behaviour:

```cpp
// UB: reinterpret_cast says "trust me" to the compiler
char buffer[sizeof(Header)];
recv(sock, buffer, sizeof(buffer), 0);
Header* h = reinterpret_cast<Header*>(buffer);   // UB on access

// Defined (C++23): start_lifetime_as actually begins
// the Header's lifetime at the buffer address
Header* h = std::start_lifetime_as<Header>(buffer);
```

The wro.cpp reflection arc walks a lot of bytes (JSON deserializer, SBOM emitter, sanitizers-2026's parse_struct), and every one of those crosses the buffer-to-struct boundary. This is the C++23 facility the next quarterly refresh of our memory-safety + hardened-stdlib + lifetime-safety toolset entries needs to add.

https://wrocpp.github.io/posts/fertig-reinterpret-cast/

## Hashtags
#cpp #cpp23 #reinterpretcast #startlifetimeas #typepunning #memorysafety #fertig #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Fertig: this is not the cast you're looking for". Subhead: C++23 std::start_lifetime_as is the object-lifetime facility reinterpret_cast cannot be. Citation: wro.cpp 2026-05-21.

## Suggested post time
Thursday 2026-05-21, 10:00 CET
Reason: Mid-week morning EU C++ + embedded audience; news short slot between Tue 5/19 (cpp-fastest-growing) and Fri 5/22 (clap-for-cpp).
