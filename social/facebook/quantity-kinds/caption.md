# One per second is not one per second

## Body
144 Hz, 144 Bq, 144 rad/s. A display refresh, a radioactive decay rate, an angular velocity. Reduce them to dimensions and all three are 1/s, so a units library that only checks dimensions will happily add a refresh rate to a radiation reading and return a well-typed, meaningless number.

mp-units adds quantity kinds from ISO 80000, same dimension and different meaning. Adding a frequency to an activity stops compiling, and you cannot build a becquerel from a hertz. Inverting the refresh rate to get a period still works, because physics allows it.

Dimensional analysis sees the dimension. mp-units sees the quantity.

https://wrocpp.github.io/posts/quantity-kinds/

## Hashtags
#cpp #cplusplus #cpp29 #mpunits #typesafety #safety #wg21

## Alt-text
A dark wro.cpp-branded social card titled "One per second is not one per second," explaining that Hz, Bq, and rad/s share the dimension 1/s but mp-units keeps them as distinct quantity kinds so mixing them does not compile.

## Suggested post time
Wednesday 2026-08-12, 10:00 CET
Reason: post lands on its own pubDate; Wednesday mid-morning CET catches the EU working-C++ audience.
