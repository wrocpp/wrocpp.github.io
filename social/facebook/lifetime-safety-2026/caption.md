# Lifetime safety in C++ 2026

## Body
Bounds and null are settled in C++26. Lifetime is the hard one. The new wro.cpp toolset entry maps the 2026 toolkit: `[[clang::lifetimebound]]`, GCC `-Wdangling-*`, `gsl::not_null`, `std::scope_exit` (P0052, in C++26), the lifetime profile (P1179).

What they miss: structural dangling inside an aggregate -- a `string_view` member alongside its source `string`, struct gets moved, SV dangles. The per-call analyzers don't look inside type topology. C++26 reflection does: a consteval walker over `nonstatic_data_members_of` refuses non-owning view members without an explicit P3394 `[[=borrows_from{}]]` annotation.

https://wrocpp.github.io/toolset/lifetime-safety-2026/

## Hashtags
#cpp #cpp26 #lifetimesafety #reflection #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Lifetime safety in C++ 2026". Subhead: per-call analyzers + schema-level borrow lint. Citation: wro.cpp 2026-06-01.

## Suggested post time
Monday 2026-06-01, 10:00 CET
Reason: Monday morning EU C++ audience.
