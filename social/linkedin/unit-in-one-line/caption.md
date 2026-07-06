# A new unit in one line

## Body
In October 1958, pledges of an MIT fraternity measured the Harvard Bridge in the body lengths of their shortest member, Oliver Smoot. The result, 364.4 smoots "plus one ear," is still painted on the bridge, and one smoot is exactly 5 feet 7 inches, or 1.7018 m.

The smoot is a good stress test for a units library, because no library ships it. Real codebases are full of units the domain invented: ticks, lots, pips, sectors, TEUs, story points. If adding one is painful, the library gets fought instead of used.

In mp-units a new unit is a single declaration. One line states the name, the printing symbol, and the exact magnitude as a rational factor of the metre, with no floating-point conversion constant to drift. Everything else is available at once, because the SI units are defined the same way rather than baked into the engine as special cases. The new unit composes with the whole system: derived quantities, kind checking, and the affine machinery all apply the moment it exists.

Episode 4 of our mp-units series, with a runnable demo.

https://wrocpp.github.io/posts/unit-in-one-line/

## Hashtags
#cpp #cplusplus #cpp26 #cpp29 #mpunits #units #extensibility

## Alt-text
A cream wro.cpp-branded social card titled "A new unit in one line" about defining a custom mp-units unit, the smoot, in a single declaration.

## Suggested post time
Wednesday 2026-09-09, 10:00 CET
Reason: post lands on its own pubDate; mid-morning CET for the EU audience.
