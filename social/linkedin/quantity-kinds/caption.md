# One per second is not one per second

## Body
A display refreshes at 144 Hz, a radioactive source decays at 144 Bq, a wheel turns at 144 rad/s. Reduce all three to dimensions and you get the same thing, 1/s. A units library that checks dimensions and stops there will add a refresh rate to a radiation reading and hand you back a well-typed number that means nothing.

Classic dimensional analysis, the version most units libraries implement, sees the dimension of a quantity but not what the quantity is. The SI brochure keeps Hz and Bq as separate units on purpose, one for periodic phenomena and one for stochastic decay, and states that the two must not be interchanged. The compiler was never told.

mp-units pioneered quantity kinds. Every quantity belongs to a kind in the ISO 80000 taxonomy, and two quantities that share a dimension but differ in kind do not mix. Adding a frequency to an activity stops compiling. You cannot initialize a becquerel from a hertz. What physics allows still works, so inverting the refresh rate gives a period you can convert to milliseconds.

The Mars Climate Orbiter was the easy case, wrong unit and same quantity. This one is right dimension and wrong quantity, and only a type system that models the quantities themselves can catch it.

Episode 2 of the mp-units series.

https://wrocpp.github.io/posts/quantity-kinds/

## Hashtags
#cpp #cplusplus #cpp29 #mpunits #typesafety #safety #wg21

## Alt-text
A dark wro.cpp-branded social card titled "One per second is not one per second," explaining that Hz, Bq, and rad/s share the dimension 1/s but mp-units keeps them as distinct quantity kinds so mixing them does not compile.

## Suggested post time
Wednesday 2026-08-12, 10:00 CET
Reason: post lands on its own pubDate; Wednesday mid-morning CET catches the EU working-C++ audience.
