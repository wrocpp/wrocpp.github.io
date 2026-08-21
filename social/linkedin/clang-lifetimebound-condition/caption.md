# A dangling warning with nothing to dangle

## Body
Clang has an attribute that tells the compiler a return value borrows from an argument, so a dangling reference becomes a warning instead of a crash:

  std::string_view first_word(const std::string& s [[clang::lifetimebound]]);

That one annotation lets -Wdangling reject first_word(std::string("hi there")). It comes from WG21 paper P0936R0, was never standardised, and ships today as a vendor extension in clang 7 and later, with MSVC spelling it [[msvc::lifetimebound]].

The attribute has no off switch, and that is the problem Barry Revzin raised on the LLVM forum this month.

Put it on a function whose return type depends on the instantiation, a value_or that sometimes returns a reference into the argument and sometimes a copy, and the annotation applies unconditionally. I built the case and compiled it: a value_or returning std::string by value, called with a temporary, and clang reports

  warning: temporary whose address is used as value of local variable 'copied'
           will be destroyed at the end of the full-expression

There is nothing to dangle. The result is a copy. The program runs to completion under AddressSanitizer and prints correctly, which is the point of wiring the sanitizer into the demo rather than arguing about it. Same warning on released clang 21.1 and 22.1, so it is not a trunk artefact.

Drop the attribute and the false positive goes away, along with the ability to catch the case where value_or really does return a reference. There is no third option, which is why the proposal asks for a conditional form.

No patch and no RFC yet, so this is a problem statement rather than a feature on its way. Worth knowing where the edge is if you annotate.

Reproduction and the discussion: https://wrocpp.github.io/posts/clang-lifetimebound-condition/

## Hashtags
#cpp #cplusplus #clang #staticanalysis #safety #compilers

## Alt-text
A wro.cpp card reading "A dangling warning with nothing to dangle", about clang lifetimebound false positives.

## Suggested post time
Saturday 2026-08-22, 14:00 CET
Reason: midday CET catches the EU afternoon and the US morning.
