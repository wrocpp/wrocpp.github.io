# Reflection in the wild: April 2026 in five links

## Body
Five things happened to C++26 reflection last month. Here they are, freshest first.

GCC 16.1 shipped P2996 on 30 April, five weeks after Croydon froze the standard. `apt install gcc-16` is days away on Ubuntu. Every example from the wro.cpp series compiles on it with one include rewrite.

Glaze v7.2 became the first production-grade C++ library to swap hand-rolled metaprogramming for a P2996 backend. The 128-member cap is gone, private members work without friend declarations, and `reflect_enums` auto-serializes enums. If you ship JSON in C++ today, this upgrade pays for itself in a sprint.

Two write-ups worth your evening: Barry Revzin on `std::meta::substitute` (the primitive behind compile-time format-string parsing), and the republished Lemire/Thiesen CppCon 2025 talk on gigabyte-per-second JSON serialization that finally puts C++ ahead of Rust's serde.

For balance: nlohmann/json, magic_enum, protobuf, Cap'n Proto are still on pre-P2996 paths. Months, not days.

Full roundup with all five links: https://wrocpp.github.io/posts/april-2026-roundup/

Which of these are you trying first?

## Hashtags
#cpp #cpp26 #p2996 #wrocpp #news

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline "Reflection in the wild" with a news kind badge dated 2026-05-10. Subtitle summarises the five April 2026 reflection stories: GCC 16.1, Glaze v7.2, Revzin on meta::substitute, Lemire and Thiesen on JSON, and the libraries still catching up.

## Suggested post time
Sunday 2026-05-10, 10:00 CET
Reason: matches the post's pubDate; Sunday morning weekly-roundup slot catches the audience before the work week resets.
