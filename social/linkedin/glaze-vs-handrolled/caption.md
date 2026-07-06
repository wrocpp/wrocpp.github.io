# Glaze v7.2 vs your hand-rolled JSON: a 30-line benchmark

## Body
On 28 April Stephen Berry shipped Glaze v7.2. It is the first release whose reflection backend is standard C++26, not __PRETTY_FUNCTION__ string-scraping.

What that one swap buys you on day one:
- No 128-member cap (the old aggregate-binding tuple trick choked past 128 fields).
- Private members serialize without friend declarations or glz::meta opt-ins.
- reflect_enums round-trips enums to strings without writing glz::meta<MyEnum>.

So the question becomes: do you still bother writing your own thirty-line serializer?

I think yes, when the schema is small, the dependency budget is zero, and you want to *understand* what reflection is doing. The 30-liner walks ^^T with nonstatic_data_members_of and the splicer obj.[: m :], and after -O2 it compiles to a straight-line string builder. You own it. You debug it with a normal stepper.

But Glaze wins by roughly an order of magnitude on payloads above a few KB. Lemire and Thiesen showed the punchline at CppCon 2025: with reflection-driven codegen, C++ JSON writers crossed gigabytes per second, past serde_json, past every runtime-typed library.

Reflection retired the macro tax on every JSON library at once. It made the thirty-line teaching version a real artefact you can ship.

Full post (with both code samples and the framing on when each wins):
https://wrocpp.github.io/posts/glaze-vs-handrolled/

What's your take? Is hand-rolled JSON still worth owning in 2026?

## Hashtags
#cpp #cpp26 #json #glaze #wrocpp

## Alt-text
Light-themed wro.cpp social card titled "Glaze v7.2 vs your hand-rolled JSON" with a one-line summary about P2996 reflection retiring __PRETTY_FUNCTION__ tricks.

## Suggested post time
Wednesday 2026-05-06, 10:00 CET
Reason: midweek morning is the strongest window for technical LinkedIn engagement in the EU + UK timezone band, and matches the pubDate.
