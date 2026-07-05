# Less standard library, faster program

## Body
Jussi Pakkanen (creator of the Meson build system) rewrote a slice of the C++ standard library from scratch, dropped ISO conformance, and converted his real CapyPDF library to it. Compile time dropped about 80%, the binary shrank about 75%, and the program ran about 25% faster, all at once.

The caveats are real: no MSVC, and it does not drop into an existing std:: codebase. Even so, the slowness we blame on C++ is often the library implementation rather than the language.

Read the pros and cons: https://wrocpp.github.io/posts/leaner-standard-library/

## Hashtags
#cpp #cplusplus #cpp26 #buildtimes #performance

## Alt-text
A dark wro.cpp social card headlined "Less standard library, faster program" with a one-line sub-claim about Pystd cutting compile time and binary size while speeding the program up.

## Suggested post time
Tuesday 2026-07-14, 10:00 CET
Reason: post lands on the post's own pubDate; Tuesday mid-morning CET catches the EU working-C++ audience.
