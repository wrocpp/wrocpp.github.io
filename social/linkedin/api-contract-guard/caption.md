# A missing guard is a property of the API you called

## Body
An AI review of Giovanni Dicanio's WinReg library said a zero-length registry string would crash four getters. The string getters have no zero check, while the binary getters do. The review was wrong, and the reason is one call down.

The string getters call RegGetValueW, which adds a terminator when the stored bytes lack one and counts it in the size. The size is never zero. RegQueryValueExW makes neither promise, so the same reader code computes 0 minus 1 there.

The post has a demo that models both contracts, since the registry API is not on Compiler Explorer. One unguarded reader gives two different answers.

https://wrocpp.github.io/posts/api-contract-guard/

## Hashtags
#cpp #cplusplus #windows #codereview #winreg #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "The missing guard was one call down" with a subtitle saying RegGetValueW promises a terminator and RegQueryValueExW does not. Citation footer: wro.cpp, 2026-10-29.

## Suggested post time
Sunday 2026-11-22, 08:00 UTC
Reason: the morning slot of a day with one post, moved here from 30 October for the MSVC post and placed after the Búzios week.
