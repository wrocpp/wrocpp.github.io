# MSVC 14.52 is a long-term release, and the 14.53 preview fixes a hardening ticket

## Body
Microsoft announced MSVC Build Tools 14.52 as generally available on 16 November, as a long-term support release that the announcement says was not scheduled to be one. It ships with Visual Studio 18.12 and the 18.11 LTSC, both released on 10 November.

The November preview of 14.53 lists a fixed ticket: "MSVC fails to cold-path _MSVC_STL_HARDENING bounds checks, hurting performance". The post gives the title only, so I make no claim about the fix.

What I could run was MSVC 19.51 on Compiler Explorer. With _MSVC_STL_HARDENING=1, a read one past the end of a vector or a span stops the process with 0xC0000409. Without it, the same read printed 0. In a gather loop the hardened build kept the failure block after the return, and replaced the plain build's SSE loop, four elements per iteration, with a scalar one. No timings.

Hardening is still off by default in the Microsoft STL. The post ends with four things to do, from turning it on in release builds to rebuilding hot loops when 14.53 ships.

https://wrocpp.github.io/posts/msvc-stl-hardening-cold-path-14-53/

## Hashtags
#cpp #msvc #hardening #memorysafety #visualstudio #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "MSVC's STL bounds checks still ship off" with a subtitle about 14.52 as a long-term release, the 14.53 preview ticket and a hardened read that stops with 0xC0000409 on MSVC 19.51. Citation footer: wro.cpp, 2026-12-01.

## Suggested post time
Tuesday 2026-12-01, 16:00 UTC
Reason: the second slot of the day, beside the 08:00 UTC tidy-agent episode.
