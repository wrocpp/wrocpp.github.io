# JSON -> struct with std::expected errors

## Body
Inverse of post 8: take untrusted JSON, build a typed struct, fail closed on bad input with path-aware errors. `std::expected<User, parse_error>` -- no exceptions, no out-parameters. Unknown fields rejected by default (trust-boundary safe); opt-in `[[=json::allow_unknown{}]]` annotation when you genuinely want lenient parsing.

Series post 10 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/json-deserialize/

## Hashtags
#cpp #cpp26 #reflection #json #expected #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "JSON to struct with std::expected errors". Subhead: Path-aware error reporting, fail-closed unknown-field rejection. Citation: wro.cpp 2026-05-15.

## Suggested post time
Friday 2026-05-15, 10:00 CET
Reason: Friday morning slot for EU audience.
