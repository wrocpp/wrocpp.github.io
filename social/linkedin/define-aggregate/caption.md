# Pick / Omit / Partial in C++26: type synthesis from struct shape

## Body
TypeScript's mapped types let you write `Pick<User, "name" | "age">` and get a new type with exactly those fields. Rust's struct update syntax lets you spread one struct into another with overrides. C++ until 2026 had nothing comparable. You wrote the new struct by hand, kept it in sync by hand, regretted it by hand when the schema drifted.

C++26 reflection ships `std::meta::define_aggregate`: declare a new type at compile time from a list of `meta::info` member descriptors. Combined with `nonstatic_data_members_of`, you can synthesise types from struct shape:

```cpp
struct User {
    std::string name;
    int         age;
    bool        admin;
    std::string email;     // sensitive -- often want to omit in DTOs
    std::string phone;
};

// New type with exactly {name, age, admin}, derived from User.
using UserDto = Pick<User, "name", "age", "admin">;

UserDto dto{"filip", 40, true};   // works -- it's an aggregate of those fields
```

The post walks the implementation: `Pick<T, Names...>` builds a `vector<data_member_spec>` filtering T's members by name, passes it to `define_aggregate(^^Tag, specs)`, returns the spliced type. The same pattern produces `Omit<T, Names...>` (everything except) and `Partial<T>` (every field wrapped in `std::optional`). The TypeScript utility types translated to C++.

Honest scope: type synthesis via `define_aggregate` is experimental in clang-p2996 / GCC 16.1 as of the post date; the full Pick / Omit / Partial story lands when the compiler context relaxes (a known restriction tracked in the P2996 implementation list). The post is upfront about which pieces work today vs which need the next compiler bump.

What this unlocks: DTOs without a separate type definition, Partial<T> for HTTP PATCH endpoints, schema migrations that synthesise the new type from the old, ORM projection types from the entity definition.

Series post 16 of 25 in the wro.cpp C++26 reflection arc.

https://wrocpp.github.io/posts/define-aggregate/

## Hashtags
#cpp #cpp26 #reflection #typesynthesis #dto #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Pick / Omit / Partial in C++26". Subhead: define_aggregate synthesises new types from struct shape; TypeScript utility types translated to C++. Citation: wro.cpp 2026-06-07.

## Suggested post time
Sunday 2026-06-07, 10:00 CET
Reason: Sunday morning slot catches weekend C++ readers; reflection-arc post 16 continues the 2-day cadence.
