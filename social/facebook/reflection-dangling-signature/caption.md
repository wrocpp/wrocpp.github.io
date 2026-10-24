# Reflection can flag a dangling signature that GCC 16.2 does not warn about

## Body
A reflection lint of under 60 lines flags a function that returns a view of a by-value string, a dangling bug that GCC 16.2 does not warn about with -Wall -Wextra. AddressSanitizer reports it only when the code runs. The lint reads signatures only, so it reports a risk and not a proof.

https://wrocpp.github.io/posts/reflection-dangling-signature/

## Hashtags
#cpp #cpp26 #reflection #memorysafety #gcc #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Reflection sees the dangling view GCC 16.2 misses" with a subtitle saying a short lint flags a view returned from a by-value owner and -Wall -Wextra says nothing. Citation footer: wro.cpp, 2026-10-29.

## Suggested post time
Monday 2026-11-02, 16:00 UTC
Reason: the second slot of the day, moved here from 29 October for the Qt flagship.
