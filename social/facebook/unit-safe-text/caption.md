# The unit travels with the value

## Body
Every codebase has a comment like "speed in m/s" above a log call. Two refactors later the calculation moved to km/h, the comment stayed, and the log now prints the wrong unit beside a correct number.

mp-units plugs a quantity straight into std::format and prints the unit symbol off the type, so the string never has to name it. When you want precision, the format grammar addresses the number and the unit separately: {::N[.2f]} rounds the numeric part and leaves the symbol alone. Convert the quantity and the log line, the UI label, and the telemetry all follow.

Episode 5 of the mp-units series, with runnable code.

https://wrocpp.github.io/posts/unit-safe-text/

## Hashtags
#cpp #cpp23 #mpunits #units #stdformat #cpp29

## Alt-text
A dark wro.cpp card titled "The unit travels with the value", noting that mp-units prints the unit symbol from a quantity's type through std::format, so changing the unit updates every log line.

## Suggested post time
Wednesday 2026-09-23, 11:00 CET
Reason: late-morning mid-week fits Facebook's more casual browsing, just after the LinkedIn slot so the two channels do not overlap.
