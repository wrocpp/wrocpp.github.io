# Making your own type allocator-aware needs a second constructor

## Body
Every pmr example tends to use a standard container. The moment you put a pmr::string or pmr::vector inside a struct of your own, you inherit an obligation: pass the allocator down to the members, or they allocate from the default resource while the object around them lives in an arena.

An allocator-aware type has three parts. It declares an allocator_type. It takes an optional allocator argument in its constructors. And it forwards that allocator to each member that can use one.

In the demo, a Record holds a pmr::string. Its normal constructor takes a trailing allocator and passes it to the string. It also has a second constructor, the allocator-extended copy: same value, but built with a caller-supplied allocator. That is the secret twin every constructor grows once a type is allocator-aware, and it is what lets a pmr::vector<Record> place each element's string in the same arena.

This is uses-allocator construction: when the vector builds a Record, it checks for an allocator_type and appends its own allocator to the call, so one arena reaches all the way to the innermost string. Miss a link in that chain and the memory escapes to the default heap there. The cost of pmr is a design cost, not a runtime one, and your own types have to opt in.

Episode 7 of the pmr series.

https://wrocpp.github.io/posts/pmr-allocator-aware/

## Hashtags
#cpp #cplusplus #cpp17 #pmr #memory #allocators #moderncpp

## Alt-text
A cream wro.cpp card reading "Every constructor needs a secret twin", on making a type allocator-aware.

## Suggested post time
Wednesday 2026-10-14, 10:00 CET
Reason: midweek morning CET; matches the series cadence.
