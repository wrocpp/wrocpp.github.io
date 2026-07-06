# The unit travels with the value

## Body
Every codebase has a comment like "speed in m/s" sitting above a log call. Two refactors later the calculation moved to km/h, the comment stayed put, and the log now prints the wrong unit next to a correct number. The next person to read that line loses an afternoon on it.

mp-units closes that gap by refusing to let the format string claim a unit the type does not back. A quantity plugs straight into std::format, and the default spec prints the unit symbol off the type. You write the value into the string and get "120 km/h" back without ever typing the unit yourself.

When you need to control precision, the quantity grammar lets you address the number and the unit separately. {::N[.2f]} applies .2f to the numeric part alone, so the same spec prints "120.00 km/h" for one quantity and "33.33 m/s" for another. The rounding request and the unit are handled independently.

The result is that a refactor cannot quietly desync the text from the value. Convert the quantity once and the log line, the UI label, and the telemetry all convert with it. The Mars Climate Orbiter failure lived at exactly this boundary, in the numbers one team's software handed to another's.

Episode 5 of the mp-units series walks through the format grammar with runnable code.

https://wrocpp.github.io/posts/unit-safe-text/

## Hashtags
#cpp #cpp23 #mpunits #units #stdformat #cpp29

## Alt-text
A dark wro.cpp card titled "The unit travels with the value", noting that mp-units prints the unit symbol from a quantity's type through std::format, so changing the unit updates every log line.

## Suggested post time
Wednesday 2026-09-23, 10:00 CET
Reason: mid-week morning catches the European C++ audience at their desks, and it matches the post's own publication day.
