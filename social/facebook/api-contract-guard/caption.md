# A missing guard is a property of the API you called

## Body
A code review flagged a missing zero check in a Windows registry wrapper. The check was not needed, because the function underneath promises a terminator and the older sibling does not. A demo models both contracts and shows one reader giving two answers.

https://wrocpp.github.io/posts/api-contract-guard/

## Hashtags
#cpp #cplusplus #windows #codereview #winreg #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "The missing guard was one call down" with a subtitle saying RegGetValueW promises a terminator and RegQueryValueExW does not. Citation footer: wro.cpp, 2026-10-29.

## Suggested post time
Thursday 2026-10-29, 08:00 UTC
Reason: single post of the day.
