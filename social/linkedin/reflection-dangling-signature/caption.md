# Reflection can flag a dangling signature that GCC 16.2 does not warn about

## Body
Klaus Iglberger's first article on C++ safety asks how you can know code is safe by reading it. A function signature can answer part of that.

On GCC 16.2, a reflection lint of under 60 lines walks a namespace and flags 3 of 5 declarations: two return a view of a by-value owner, one returns a const reference that can bind a temporary argument. For the view case, -Wall -Wextra gives no warning, a plain run prints a view that no longer matches its source, and AddressSanitizer reports a heap use after free.

The lint reads signatures only, so it reports a risk and proves nothing about the body. The post shows the demos on GCC 16.2 and trunk, and the limits.

https://wrocpp.github.io/posts/reflection-dangling-signature/

## Hashtags
#cpp #cpp26 #reflection #memorysafety #gcc #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "Reflection sees the dangling view GCC 16.2 misses" with a subtitle saying a short lint flags a view returned from a by-value owner and -Wall -Wextra says nothing. Citation footer: wro.cpp, 2026-10-29.

## Suggested post time
Thursday 2026-10-29, 16:00 UTC
Reason: second post of the day; the API contract post holds the 08:00 UTC slot.
