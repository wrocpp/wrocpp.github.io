# Handling overflow and division by zero without undefined behavior

## Body
INT_MAX + 1 can clamp, report or trap, depending on the tool. std::saturating_add clamps to INT_MAX. ckd_add returns the wrapped value and a flag. -ftrapv stops the program. Each was run on GCC 16.2, with the exact diagnostics.

The post also shows a build where -ftrapv does not trap, what x / 0 does in a constant expression, and which standard libraries have these functions.

https://wrocpp.github.io/posts/handle-overflow-and-division-by-zero-without-ub/

## Hashtags
#cpp #cpp26 #undefinedbehavior #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "INT_MAX + 1 can clamp, report or trap" with a subtitle naming std::saturating_add, ckd_add and -ftrapv as three different policies run on GCC 16.2. Citation footer: wro.cpp, 2026-11-06.

## Suggested post time
Friday 2026-11-06, 08:00 UTC (09:00 CET)
Reason: one short post for the day, in the ub-checks-per-statement series.
