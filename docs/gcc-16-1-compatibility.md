# GCC 16.1 compatibility matrix

_Generated 2026-05-01 by `scripts/gcc-compatibility-report.py`._

Compiler: GCC 16.1 on Compiler Explorer (id `g161`), released April 2026.
Flags: `-std=c++26 -freflection`

## Source rewrites applied

The .cpp on disk targets clang-p2996 (uses `<experimental/meta>`); the
audit applies these rewrites in-memory before sending to GCC:

- `<experimental/meta>` -> `<meta>`

## Summary

**15 / 28 OK; 1 output-drift; 12 compile-fail; 0 exec-fail**

## Per-example matrix

| # | Slug | Variant | Status | Category | Notes |
|---|------|---------|--------|----------|-------|
| 1 | `why-cpp26-reflection-matters` | `teaser` | OK | ok | matches clang stdout |
| 1 | `why-cpp26-reflection-matters` | `teaser_annotated` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 1 | `why-cpp26-reflection-matters` | `teaser_formats` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 1 | `why-cpp26-reflection-matters` | `teaser_peel` | OK | ok | matches clang stdout |
| 2 | `first-reflection` | `describe` | OUTPUT_DRIFT | runtime-diff | clang first line: 'Point:'; gcc: 'Point:' |
| 3 | `splicing` | `splice_basics` | COMPILE_FAIL | consteval-strict | 'members' is not a constant expression |
| 4 | `template-for-expansion-statements` | `dump` | COMPILE_FAIL | consteval-strict | modification of '<anonymous>' from outside current evaluation is not a constant expression |
| 5 | `enum-to-string` | `renum` | OK | ok | ran cleanly (no clang baseline) |
| 6 | `auto-formatter` | `formatter` | OK | ok | ran cleanly (no clang baseline) |
| 7 | `derive-eq-hash` | `hash_demo` | OK | ok | ran cleanly (no clang baseline) |
| 8 | `json-naive` | `rjson` | OK | ok | ran cleanly (no clang baseline) |
| 9 | `annotations` | `annotated` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 10 | `json-deserialize` | `from_values` | OK | ok | ran cleanly (no clang baseline) |
| 11 | `one-codegen-many-formats` | `formats_demo` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 12 | `clap-for-cpp` | `cli_demo` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 13 | `tiny-orm` | `sql_gen` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 14 | `dependency-injection` | `di_demo` | OK | ok | ran cleanly (no clang baseline) |
| 15 | `auto-mocks` | `mock_demo` | OK | ok | ran cleanly (no clang baseline) |
| 16 | `define-aggregate` | `pick` | OK | ok | ran cleanly (no clang baseline) |
| 17 | `qt-moc-replacement` | `properties` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 18 | `cross-language-comparison` | `main` | OK | ok | ran cleanly (no clang baseline) |
| 19 | `reflect-llmschema` | `llmschema` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 20 | `reflect-arbitrary` | `arbitrary` | OK | ok | ran cleanly (no clang baseline) |
| 21 | `reflect-optics` | `optics` | OK | ok | ran cleanly (no clang baseline) |
| 22 | `reflect-dx` | `natvis_emit` | OK | ok | ran cleanly (no clang baseline) |
| 23 | `reflect-telemetry` | `prometheus_emit` | COMPILE_FAIL | api-name-diff | 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtem |
| 24 | `reflect-tracing` | `trace_emit` | COMPILE_FAIL | api-name-diff | no matching function for call to 'define_static_string(const char*)' |
| 25 | `reflect-soa` | `soa` | OK | ok | ran cleanly (no clang baseline) |

## Failure detail

### 01 `why-cpp26-reflection-matters` / `teaser_annotated` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'consteval std::string_view rjson::key_of()':
<source>:72:49: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   72 |     if constexpr (constexpr auto a = std::meta::annotation_of_type<json_name_tag>(Member)) {
      |                                                 ^~~~~~~~~~~~~~~~~~
      |              
```

### 01 `why-cpp26-reflection-matters` / `teaser_formats` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'consteval std::string_view rserial::key_of()':
<source>:57:32: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   57 |                   = std::meta::annotation_of_type<json_name_tag>(Member)) {
      |                                ^~~~~~~~~~~~~~~~~~
      |                                annotations_of
```

### 02 `first-reflection` / `describe` -- OUTPUT_DRIFT

Category: **runtime-diff**

```
--- clang expected ---
Point:
x: int
y: int

Line:
a: Point
b: Point
name: basic_string<char, char_traits<char>, allocator<char>>

--- gcc actual ---
Point:
x: int
y: int

Line:
a: Point
b: Point
name: std::__cxx11::basic_string<char>

```

### 03 `splicing` / `splice_basics` -- COMPILE_FAIL

Category: **consteval-strict**

```
<source>: In instantiation of 'void dump(const T&) [with T = Point]':
<source>:40:9:   required from here
   40 |     dump(p);
      |     ~~~~^~~
<source>:29:38: error: 'members' is not a constant expression
   29 |     template for (constexpr auto m : members) {
      |                                      ^~~~~~~
<source>:29:38: note: reference to 'members' is not a constant expression
<source>
```

### 04 `template-for-expansion-statements` / `dump` -- COMPILE_FAIL

Category: **consteval-strict**

```
<source>: In function 'int main()':
<source>:32:5: error: modification of '<anonymous>' from outside current evaluation is not a constant expression
   32 |     }
      |     ^
```

### 09 `annotations` / `annotated` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'consteval std::string_view rjson::key_of()':
<source>:51:49: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   51 |     if constexpr (constexpr auto a = std::meta::annotation_of_type<json_name_tag>(Member)) {
      |                                                 ^~~~~~~~~~~~~~~~~~
      |              
```

### 11 `one-codegen-many-formats` / `formats_demo` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'consteval std::string_view rserial::key_of()':
<source>:57:32: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   57 |                   = std::meta::annotation_of_type<json_name_tag>(Member)) {
      |                                ^~~~~~~~~~~~~~~~~~
      |                                annotations_of
```

### 12 `clap-for-cpp` / `cli_demo` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'Args cli::parse(std::span<const std::basic_string_view<char> >)':
<source>:42:39: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   42 |             if constexpr (!std::meta::annotation_of_type<positional>(m).has_value()) {
      |                                       ^~~~~~~~~~~~~~~~~~
      |         
```

### 13 `tiny-orm` / `sql_gen` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'consteval const char* orm::table_name_of()':
<source>:42:49: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   42 |     if constexpr (constexpr auto a = std::meta::annotation_of_type<table_tag>(^^T))
      |                                                 ^~~~~~~~~~~~~~~~~~
      |                       
```

### 17 `qt-moc-replacement` / `properties` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'std::vector<rqt::property_info> rqt::properties_of()':
<source>:37:34: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   37 |         if constexpr (std::meta::annotation_of_type<property>(m).has_value()) {
      |                                  ^~~~~~~~~~~~~~~~~~
      |                                
```

### 19 `reflect-llmschema` / `llmschema` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'consteval const char* llm::openai_tool_json(std::string_view)':
<source>:73:32: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   73 |                   = std::meta::annotation_of_type<description_tag>(^^ArgsStruct)) {
      |                                ^~~~~~~~~~~~~~~~~~
      |                     
```

### 23 `reflect-telemetry` / `prometheus_emit` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'std::string metrics::expose_prometheus(const T&)':
<source>:38:41: error: 'annotation_of_type' is not a member of 'std::meta'; did you mean 'annotations_of_with_type'? [-Wtemplate-body]
   38 |     constexpr auto type_ns = std::meta::annotation_of_type<namespace_tag>(^^T);
      |                                         ^~~~~~~~~~~~~~~~~~
      |                             
```

### 24 `reflect-tracing` / `trace_emit` -- COMPILE_FAIL

Category: **api-name-diff**

```
<source>: In function 'void with_nttp_named()':
<source>:209:65: error: no matching function for call to 'define_static_string(const char*)'
  209 |     static constexpr char const* _fn = std::define_static_string(
      |                                        ~~~~~~~~~~~~~~~~~~~~~~~~~^
  210 |         std::source_location::current().function_name());
      |         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

## Compiler-support footer

Posts confirmed to run on **clang-p2996 + GCC 16.1**:

- `auto-formatter`
- `auto-mocks`
- `cross-language-comparison`
- `define-aggregate`
- `dependency-injection`
- `derive-eq-hash`
- `enum-to-string`
- `first-reflection`
- `json-deserialize`
- `json-naive`
- `reflect-arbitrary`
- `reflect-dx`
- `reflect-optics`
- `reflect-soa`

Posts that currently ship as **clang-p2996 only**:

- `annotations`
- `clap-for-cpp`
- `one-codegen-many-formats`
- `qt-moc-replacement`
- `reflect-llmschema`
- `reflect-telemetry`
- `reflect-tracing`
- `splicing`
- `template-for-expansion-statements`
- `tiny-orm`
- `why-cpp26-reflection-matters`
