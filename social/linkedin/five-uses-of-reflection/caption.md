# The five most useful things C++26 reflection unlocks (in effort order)

## Body
C++26 reflection looks like it requires a PhD in template metaprogramming. It does not. Five concrete projects you can build with it -- ranked from "5 minutes" to "weeks". Use this list as a triage when you pick your first reflection-powered project.

The list:

1. enum-to-string -- 5 minutes. Twelve lines, no `magic_enum`, no `__PRETTY_FUNCTION__` parsing trick. The smallest possible win and the one that retires the most legacy code.

2. struct-to-JSON -- 1 hour. Forty lines and `to_json(T)` works for any aggregate. No `NLOHMANN_DEFINE_TYPE_INTRUSIVE` macros, no Boost.Describe registration block, no codegen step.

3. derived equality + hash -- 1 hour. C++20 gave us `= default` for `==` and `<=>` but never `std::hash`. Reflection closes the gap with one source of truth across equality, ordering, and hashing.

4. dependency injection container -- 1 day. Spring-style autowiring in roughly sixty lines. Reflection asks "what are the constructor parameters of T?" at compile time, looks each one up in a registry, and assembles the call.

5. domain-specific code generation -- weeks. ORMs, schema validators, CLI parsers, gRPC stubs -- all without a separate code-generator step. The open-ended payoff and the reason reflection was worth waiting for.

Pick #1 first. If it sticks, you'll naturally walk up the list.

Read it: https://wrocpp.github.io/posts/five-uses-of-reflection/

Which one are you reaching for first?

## Hashtags
#cpp #cpp26 #p2996 #moderncpp #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline reads "Five things C++26 reflection unlocks." with the plus signs in orange and a blue period. Sub-claim: ranked from 5 minutes (enum-to-string) to weeks (DSL-driven code generation), use as triage for your first reflection project. Citation: wro.cpp 2026-05-17.

## Suggested post time
Sunday 2026-05-17, 10:00 CET
Reason: matches the post's pubDate so the link goes live the same morning the teaser lands; Sunday morning is a quieter window where opinion / triage content travels well in the European C++ community.
