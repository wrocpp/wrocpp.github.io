# Turning an embedded SQL schema into checked row types

## Body
SELECT id, nme FROM users stops the build with: unknown column 'nme' in table 'users' (columns: id, name, email, age, active). No database was running. The compiler had read schema.sql.

The demo uses #embed to put the CREATE TABLE text into the program, a consteval parser to read it, and define_aggregate to make one row struct per table. Nullable columns become std::optional, a query string is checked against the schema, and a hand-written struct can be checked for drift, with a message that names the table and column.

The SQL subset is tiny: five column types, one WHERE column OP ?, no joins, no IS NULL, and enums are strings. It was tested on GCC 16.2 only, and the post compares the idea with sqlpp23 ddl2cpp, sqlgen and sqlx from their current documentation. The demo runs on Compiler Explorer.

https://wrocpp.github.io/posts/turn-embedded-sql-schema-into-row-types/

## Hashtags
#cpp #cpp26 #reflection #sql #compiletime #wrocpp

## Alt-text
Cream wro.cpp card with the magnet logo. Headline reads "The compiler read schema.sql and checked my query" with a subtitle saying that #embed and a consteval parser turn CREATE TABLE into row structs and that a wrong column name is a build error. Citation footer: wro.cpp, 2026-11-12.

## Suggested post time
Thursday 2026-11-12, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
