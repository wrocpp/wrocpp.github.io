# Less standard library, faster program

## Body
Faster builds usually cost you something later: a slower binary, a bigger one, less headroom for the optimizer. Pystd broke that pattern.

Jussi Pakkanen (creator of the Meson build system) rewrote a subset of the C++ standard library from scratch, throwing out ISO conformance to chase compile speed. Then he converted his real, shipping CapyPDF library to use it. Compile time dropped about 80%, the unstripped binary about 75%, and runtime came out about 25% faster, all at once.

Here is why. The slowness we blame on "C++" is often the library implementation rather than the language. Preprocess one #include <vector> and it blooms to ~29,000 lines; <filesystem> hits ~80,000. Less abstraction for the compiler to instantiate means a smaller binary and less runtime indirection too.

The limits are real. Pystd does not speak std::, so every boundary with the ecosystem needs a conversion; it does not build on MSVC; and it stays quiet on the hard parts (exceptions, allocators, iterator invalidation). The committee's own answer to header bloat is import std; and modules.

One discipline ports to any codebase today: a hard per-header compile budget in CI. Pystd's is 0.15s, enforced even on a Raspberry Pi.

Full breakdown (pros and cons) on wro.cpp: https://wrocpp.github.io/posts/leaner-standard-library/

Would you trade std:: conformance for an 80% faster build?

## Hashtags
#cpp #cplusplus #cpp26 #buildtimes #performance #stdlib #meson

## Alt-text
A dark wro.cpp social card headlined "Less standard library, faster program" with a one-line sub-claim about Pystd cutting compile time and binary size while speeding the program up.

## Suggested post time
Tuesday 2026-07-14, 10:00 CET
Reason: post lands on the post's own pubDate; Tuesday mid-morning CET catches the EU working-C++ audience.
