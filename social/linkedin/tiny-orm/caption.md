# A tiny ORM in 100 lines: struct -> SQL via reflection

## Body
ORMs in C++ have always been the awkward middle child. Either you ship a heavyweight library (sqlpp23, sqlite_orm, Code::Blocks ORM Lite) with its own DSL, or you handwrite `CREATE TABLE` + `INSERT INTO ... VALUES (?, ?, ?)` per type and bind the placeholders by hand. Both have failure modes when the schema changes.

C++26 reflection handles the boilerplate side cleanly. Walk a struct, emit DDL + DML statements with positional placeholders + a typed bind helper. The schema is the struct definition.

```cpp
struct User {
    [[=orm::primary_key{}, =orm::autoincrement{}]] int id;
    [[=orm::rename{"user_name"}]]                  std::string name;
    [[=orm::rename{"mail"}]]                       std::string email;
    [[=orm::rename{"is_admin"}]]                   bool admin;
};

std::println("{}", orm::create_table<User>("users"));
// CREATE TABLE users (
//   id INTEGER PRIMARY KEY AUTOINCREMENT,
//   user_name TEXT,
//   mail TEXT,
//   is_admin BOOLEAN
// );

std::println("{}", orm::insert<User>("users"));
// INSERT INTO users (user_name, mail, is_admin) VALUES (?, ?, ?);

orm::bind(stmt, user);  // walks the struct, calls sqlite3_bind_text/int/bool per field
```

What the post covers: the type -> SQL mapping (int, string, bool, optional, blob), the annotation taxonomy (`primary_key`, `autoincrement`, `not_null`, `rename`, `default_value`, `foreign_key`), the bind helper that walks via reflection and dispatches per-field to the sqlite3_bind_* family, the SELECT row-to-struct decoder with field-name -> column-index matching.

What this does NOT replace: production ORMs with migration management, query builders, eager/lazy joins, dialect-aware SQL generation. The 100-line version is for the codebase that wants ORM ergonomics for ~20 tables without taking on a library dependency.

Cross-link: this is the same annotation taxonomy as the JSON walker (post 8) + CLI parser (post 12). Schema-as-spec across formats, CLI, persistence. One struct definition, four consumers.

Series post 13 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/tiny-orm/

## Hashtags
#cpp #cpp26 #reflection #sql #orm #sqlite #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "A tiny ORM in 100 lines". Subhead: Reflection-driven struct-to-SQL with per-field annotations for primary keys, renames, defaults, and the typed bind helper. Citation: wro.cpp 2026-05-26.

## Suggested post time
Tuesday 2026-05-26, 10:00 CET
Reason: Tuesday morning slot reaches EU C++ engineers planning the week; reflection-arc post 13 demonstrates the schema-as-spec pattern crossing into persistence.
