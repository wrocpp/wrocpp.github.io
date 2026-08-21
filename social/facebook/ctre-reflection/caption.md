# One function fills any struct

## Body
A regex with N captures already describes a record with N fields, and C++26 reflection can enumerate a struct's fields. Joining them gives one helper that fills any aggregate, with no code per type.

Two unrelated structs, one function, and a non-matching input returns nullopt rather than a half-filled struct.

Positional rather than by name, and that is deliberate. Matching capture names to member names needs the identifier as a template argument, and reflection hands it back as a value. The straightforward spellings do not survive the trip. Positional sidesteps it entirely.

Episode 7 of the CTRE series: https://wrocpp.github.io/posts/ctre-reflection/

## Hashtags
#cpp #cplusplus #cpp26 #programming

## Alt-text
A wro.cpp card about combining CTRE with C++26 reflection.

## Suggested post time
Saturday 2026-10-03, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
