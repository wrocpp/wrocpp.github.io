# Boost starts shipping modules, one library at a time

## Body
In June the state of modules came down to one sentence: import std works, and import boost is coming. Boost 1.92.0, released 12 August, is the first instalment of the second half.

Six libraries gained C++20 module support: Conversion, DLL, LexicalCast, PFR, Stacktrace and TypeIndex. Out of roughly 180 Boost libraries that is a rounding error. The mechanism they chose is what makes it worth writing about.

The obvious way to add module support is to publish a module and let users migrate. Every include becomes an import, across every file, all at once, and you find out afterwards whether the build got faster.

Boost did something less disruptive. Build with the CMake option BOOST_USE_MODULES=1 and, per the TypeIndex documentation, all the boost/type_index includes implicitly do import boost.type_index. Your source keeps saying include. The header notices the macro and forwards to the module.

That trick is the part worth stealing. Modules have an adoption problem that has nothing to do with whether they work: a large codebase cannot flip from includes to imports incrementally without ending up half migrated, with both spellings live and the build system coping with each. Making a macro do the switch turns a source migration into a build flag experiment. Turn it on, measure, turn it off if it disappoints.

Boost is not overselling it. The documentation says module support is at an early stage and that targets, flags and behaviour may change. It also notes you want import std available when building the module for the best compile times, which restates the dependency that has held modules back everywhere: the payoff arrives when the whole chain is modularised, not when one link is.

Nobody should rewrite a build on this yet. What changed is the shape of the problem. A year ago the honest answer about Boost and modules was that the work had not started in a form you could try.

https://wrocpp.github.io/posts/boost-modules-1-92/

Have you measured modules on a real codebase yet?

## Hashtags
#cpp #cplusplus #boost #cpp20 #modules

## Alt-text
A wro.cpp social card reading "Your includes become imports", about Boost 1.92 adding C++20 module support to six libraries.

## Suggested post time
Sunday 2026-10-26, 11:00 CET
Reason: Weekend late morning for a build systems read.
