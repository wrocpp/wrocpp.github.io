# Closing the known limits of the Qt observable models

## Body
Ten limits were left open in the last Qt post. Most are closed now, and tests found three real defects on the way.

The most instructive one: a hash removal that looked 1.7 times slower with typed signals was the same loop landing across a 32-byte boundary in one build. Padding either build made them equal.

A row index also makes a change 42 to 125 times cheaper at large sizes, and QMultiMap works.

https://wrocpp.github.io/posts/qt-observable-models-known-limits/

## Hashtags
#cpp #qt #reflection #performance #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A 1.7x slowdown that was only code placement". Citation footer: wro.cpp, 2026-10-28.

## Suggested post time
Wednesday 2026-10-28, 16:00 UTC
Reason: second post of the day; the planned-double slot in scripts/schedule_doubles.py.
