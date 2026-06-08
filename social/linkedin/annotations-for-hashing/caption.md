# Annotations for hashing: opt out of fields, not whole structs

## Body
Krystian Piekos's May 29 post on infotraining.pl shows the cleanest demo so far of P3394 annotations combined with P2996 reflection.

The pattern: opt structs into hashing with [[=hashable]]. Skip individual fields or base classes with [[=skipped_for_hash]]. The Hashable concept gates the template; the calculate_hash walker filters via annotations_of_with_type. Forty lines total. No macros. No std::hash<T> specializations to maintain.

Why this matters: writing your own hash almost always means writing "combine these fields, but not those." Without reflection you write the function by hand or hack a macro. With reflection alone you get all-or-nothing. Annotations bridge the gap.

The same pattern composes with simdjson's [[simdjson::skip]] and the tiny-orm [[pk]] / [[no_insert]] annotations from earlier posts in the series. One annotation, used by every reflection-driven helper that cares.

https://wrocpp.github.io/posts/annotations-for-hashing/

## Hashtags
#cpp #cpp26 #reflection #p2996 #p3394 #annotations #hashing #wrocpp

## Alt-text
Editorial card: "Annotations for hashing: opt out fields, not whole structs". P3394 + P2996 demo by Krystian Piekos.

## Suggested post time
Saturday 2026-06-20, 10:00 CET
