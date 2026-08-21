# A dangling warning with nothing to dangle

## Body
Clang's [[clang::lifetimebound]] tells the compiler a result borrows from an argument, so -Wdangling can catch a string_view into a temporary. Useful, and it has no off switch.

Put it on a value_or that returns a copy on some instantiations and a reference on others, and it applies unconditionally. I compiled the case: a value_or returning std::string by value, called with a temporary, warns about a dangling temporary even though the result is a copy. The program runs clean under AddressSanitizer, which is how you know the warning is spurious rather than by arguing about it.

Remove the attribute and you lose the real dangle detection too. Barry Revzin has proposed a conditional form; there is no patch yet.

Reproduction on released clang: https://wrocpp.github.io/posts/clang-lifetimebound-condition/

## Hashtags
#cpp #cplusplus #clang #programming

## Alt-text
A wro.cpp card about clang lifetimebound producing a false positive.

## Suggested post time
Saturday 2026-08-22, 14:00 CET
Reason: midday CET catches the EU afternoon and the US morning.
