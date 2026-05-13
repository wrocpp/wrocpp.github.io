# Lifetime safety in C++ 2026: per-call analyzers + the schema-level borrow lint

## Body
Bounds and null are settled in C++26. Bounds: flip the hardened stdlib macro and `vector::operator[]` aborts on OOB. Null: `std::expected`, `gsl::not_null`, dereference checks. **Lifetime is the hard one.** A `string_view` returned from a function that built a local `string`, a struct that holds a view next to its source then gets moved, a coroutine that captures a reference and resumes after the referent vanishes -- the failure modes are everywhere, the diagnostics uneven across compilers.

The 2026 toolkit (no reflection needed):
- **`[[clang::lifetimebound]]`** on parameters / return values -- Clang + MSVC catch return-of-local-view, temporary-bound-to-view-param, store-reference-to-temporary
- **GCC `-Wdangling-reference` / `-Wdangling-pointer`** (since GCC 13) -- less precise but always-on
- **`gsl::not_null<T*>`** -- type-level non-null
- **`std::scope_exit`** (P0052, ratified into C++26) -- standard-library scope guards
- **The C++ Core Guidelines lifetime profile** (P1179) -- implemented as the `[[clang::lifetime_capture_by]]` family

What they all miss: **structural dangling inside an aggregate**. A struct with a `string_view` member alongside a sibling `string` member, with the constructor pointing the SV at the string. Move the struct, SV dangles. The per-call analyzer never looks inside the type's lifetime topology.

C++26 reflection closes the gap. A consteval predicate walks `nonstatic_data_members_of(^^T)` and refuses to compile when any non-owning view member (`string_view`, `span`, reference, raw pointer) lacks a P3394 `[[=borrows_from{}]]` annotation. The annotation has no runtime effect -- it forces the developer to encode borrow intent at the type level so a reviewer can argue "this view cannot dangle" without reading the constructor.

The walker pattern composes with the [hardened-stdlib schema lint](https://wrocpp.github.io/toolset/hardened-stdlib/) (no raw pointers/C-arrays) and the [qualified-compilers MISRA lint](https://wrocpp.github.io/toolset/qualified-compilers/) (members must be private). Same walker, orthogonal rules.

C++29 candidate features collapse it further: `[[profiles::enforce(lifetime)]]` (P3081/P3589/P3984) moves lifetime checks into compiler-enforced subsets; P3294 token injection generates the safe-accessor wrappers alongside the borrow annotations.

https://wrocpp.github.io/toolset/lifetime-safety-2026/

## Hashtags
#cpp #cpp26 #lifetimesafety #lifetimebound #reflection #p3394 #wrocpp #moderncpp #safety

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "Lifetime safety in C++ 2026". Subhead: lifetimebound + dangling diagnostics + scope_exit + reflection-driven borrow lint that closes the structural-dangle gap. Citation: wro.cpp 2026-06-01.

## Suggested post time
Monday 2026-06-01, 10:00 CET
Reason: Monday morning EU C++ audience starts the week with the safety thread; toolset launch fits the off-day cadence between reflection-series posts.
