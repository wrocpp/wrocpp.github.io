# Quantities and units on the road to C++29

## Body
Everything the mp-units series demonstrated is also a standardization proposal.

P3045, "Quantities and units library," targets C++29 with mp-units as its reference implementation. The core of the pitch is an interface that says what it takes, not just which arithmetic type. A function declared as avg_speed(quantity<si::metre>, quantity<si::second>) accepts kilometres or hours and converts them exactly, but it will not compile if you swap the two arguments. Compare that with double avg_speed(double, double), where parameter names are the only thing standing between you and a silent wrong answer.

Multiply that across every interface in a flight controller, a medical device, or a trading system and the case for putting it in std stops being abstract. Safety this basic should not depend on which third-party library a project happened to adopt.

The lead author is Mateusz Pusz from Gdansk, a voting member of the ISO C++ committee since 2017. He co-founded the PKN subcommittee through which Poland became a P-member of ISO C++, so Poland now votes on what the language becomes. A decade of library iterations sits behind the paper, all in the open on GitHub.

Standardization is slow, and nothing is settled until the final plenary vote. If P3045 lands, the demos from this series will need nothing but import std;.

Full write-up, with the runnable Godbolt signature and the rest of the mp-units series:
https://wrocpp.github.io/posts/units-road-to-cpp29/

## Hashtags
#cpp #cpp29 #mpunits #wg21 #cppstandard #typesafety #units

## Alt-text
A dark wro.cpp card titled "Units on the road to C++29," summarizing that P3045 proposes putting mp-units in the C++ standard library with an interface that says what it takes.

## Suggested post time
Tuesday 2026-10-13, 10:00 CET
Reason: Tuesday mid-morning catches the European C++ audience at the start of the week without the Monday backlog, and the US East Coast is coming online.
