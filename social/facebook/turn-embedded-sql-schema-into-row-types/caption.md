# Turning an embedded SQL schema into checked row types

## Body
The compiler read schema.sql and caught a misspelled column in a SELECT, with no database running. #embed puts the CREATE TABLE text into the program, a consteval parser reads it, and define_aggregate makes a row struct per table, with std::optional for nullable columns.

The SQL subset is tiny and the demo was tried on GCC 16.2 only. The post lists what is missing.

https://wrocpp.github.io/posts/turn-embedded-sql-schema-into-row-types/

## Hashtags
#cpp #cpp26 #reflection #sql #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "The compiler read schema.sql and checked my query" with a subtitle saying that #embed and a consteval parser turn CREATE TABLE into row structs and that a wrong column name is a build error. Citation footer: wro.cpp, 2026-11-12.

## Suggested post time
Thursday 2026-11-12, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
