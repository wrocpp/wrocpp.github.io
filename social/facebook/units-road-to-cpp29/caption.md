# Quantities and units on the road to C++29

## Body
The whole mp-units series was previewing a proposal. P3045 aims to put quantities and units into the C++29 standard library, with mp-units as the reference implementation.

The idea is an interface that says what it takes. A function taking quantity<si::metre> and quantity<si::second> accepts kilometres or hours, converts them exactly, and refuses to compile if you swap the two arguments. Plain double parameters give you none of that protection.

The lead author is Mateusz Pusz from Gdansk, an ISO C++ voting member since 2017. He co-founded the PKN subcommittee that made Poland a P-member of the committee, so Poland has a vote on what C++ becomes.

Read the series finale:
https://wrocpp.github.io/posts/units-road-to-cpp29/

## Hashtags
#cpp #cpp29 #mpunits #wg21 #typesafety

## Alt-text
A dark wro.cpp card titled "Units on the road to C++29," summarizing that P3045 proposes putting mp-units in the C++ standard library with an interface that says what it takes.

## Suggested post time
Tuesday 2026-10-13, 10:00 CET
Reason: Tuesday mid-morning fits the European C++ audience and Facebook engagement holds steady through late morning on weekdays.
