# Points are not deltas

## Body
The unit checker from the last episode will happily add 21 C and 17 C and give you 38 C. Same unit, same quantity kind, and the result is not a temperature anywhere in the world.

Dimensional analysis cannot catch it, because the dimension was never the problem. A reading and a change are different things. Mathematics has called this the affine space for a century. A point is a position against an origin: a temperature reading, a timestamp, an altitude. A delta is the gap between two points: a warming, a duration, a climb. Deltas add freely. Two points do not. Subtracting two points gives a delta, and adding a delta to a point gives a new point, and those are the only moves the algebra allows.

std::chrono users already live with this split. time_point and duration are the same idea, and nobody tries to add two timestamps. mp-units carries it to every quantity. quantity_point holds an absolute reading, quantity holds a delta, and the operations that make no physical sense fail to compile instead of returning a confident wrong answer.

Temperatures are the sharpest case, because 0 C hides an origin at the ice point. The same modeling covers positions against displacements and altitudes against climbs. When a signature passes a metre around, it can now say whether that is a metre from somewhere or a metre of difference.

Episode 3 of the mp-units series:
https://wrocpp.github.io/posts/points-are-not-deltas/

## Hashtags
#cpp #cpp23 #mpunits #units #affinespace #typesafety

## Alt-text
Dark wro.cpp card titled "Points are not deltas", with a one-line note that a temperature reading and a temperature change are different quantities and that mp-units keeps them apart in the type system.

## Suggested post time
Wednesday 2026-08-26, 10:00 CET
Reason: publication day, midweek morning catches European working-hours C++ readers scrolling LinkedIn before standups.
