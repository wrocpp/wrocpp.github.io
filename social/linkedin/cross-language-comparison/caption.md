# C++26 reflection vs Rust / Java / C# / TypeScript / Go / Python -- the capstone

## Body
Eighteen posts into the wro.cpp reflection arc. This one zooms out: five canonical reflection tasks (JSON serialize, enum -- string, CLI parse, ORM row binding, mock generation) lined up across **seven languages** -- Rust (serde), C# (System.Text.Json), Java (Jackson), TypeScript (decorators), Go (struct tags), Python (Pydantic), and **C++26**. Not to declare a winner. To be precise about what kind of reflection each gives you, at what cost, with what ceiling.

The headline finding: the **vocabulary is identical everywhere**. Spelling differs; concepts map 1:1. `[[=rjson::rename_all(rjson::naming::camel_case)]] struct User` in C++26 is the same idea as `#[serde(rename_all = "camelCase")] struct User` in Rust, `[JsonPropertyName]` in C#, `@JsonProperty` in Java, `serializedName: "..."` in TypeScript decorators. The pattern doesn't belong to any one language anymore -- C++26 just makes it native instead of a third-party library or codegen pass.

What makes C++ distinctive: **every dispatch resolves at compile time**. The binary contains no per-field attribute table. The output function for `User` is a straight-line string builder that the optimiser sees end-to-end. Rust is comparable via `proc_macro` (separate codegen phase, generated code compiled normally). Java, C#, Python, Go all do the walk at runtime. The cost model is the most distinctive thing here, not the syntax.

What this does NOT claim: that C++26 is "better than" any of the others. Each language picked a different point on the (compile-time work, runtime work, ergonomics, ecosystem maturity) curve. Rust's macro story is more mature. Java's runtime ecosystem is bigger. The post is honest about which axes C++26 wins, which it draws, and which others still lead.

Series post 18 of 25 in the wro.cpp C++26 reflection arc -- the capstone of the "what does reflection unlock" thread before the second-half deep-dives. Live demo on Godbolt with clang-p2996.

https://wrocpp.github.io/posts/cross-language-comparison/

## Hashtags
#cpp #cpp26 #reflection #rust #java #csharp #typescript #python #golang #wrocpp #moderncpp

## Alt-text
Dark editorial card with the wro.cpp magnet wordmark. Headline: "C++26 reflection across seven languages". Subhead: serialize, enum-to-string, CLI, ORM, mocks side-by-side in Rust, C#, Java, TypeScript, Go, Python, C++26. Citation: wro.cpp 2026-06-15.

## Suggested post time
Monday 2026-06-15, 10:00 CET
Reason: Monday morning EU audience opens the second half of the reflection arc. Capstone post deserves Monday slot.
