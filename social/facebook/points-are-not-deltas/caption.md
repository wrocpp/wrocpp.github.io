# Points are not deltas

## Body
"21 degrees" and "21 degrees warmer" are not the same quantity. One is a reading, the other is a change. Adding two readings is meaningless even when the units line up, so 21 C plus 17 C is 38 C on paper and nothing outside it.

Mathematics calls this the affine space. A point sits against an origin, a delta is the distance between two points. std::chrono users know the split as time_point versus duration. mp-units brings it to every quantity: quantity_point for an absolute reading, quantity for a delta. Point plus delta compiles. Point plus point does not.

Episode 3 of the mp-units series:
https://wrocpp.github.io/posts/points-are-not-deltas/

## Hashtags
#cpp #cpp23 #mpunits #units #affinespace #typesafety

## Alt-text
Dark wro.cpp card titled "Points are not deltas", with a one-line note that a temperature reading and a temperature change are different quantities and that mp-units keeps them apart in the type system.

## Suggested post time
Wednesday 2026-08-26, 18:00 CET
Reason: publication day, early evening is when the Facebook community page sees the most non-work scrolling in the CET timezone.
