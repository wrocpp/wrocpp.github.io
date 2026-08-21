# Boost starts shipping modules, one library at a time

## Body
In June the state of modules was one sentence: import std works, import boost is coming. Boost 1.92.0, released 12 August, is the first instalment of the second half.

Six libraries gained C++20 module support: Conversion, DLL, LexicalCast, PFR, Stacktrace and TypeIndex. Out of roughly 180 Boost libraries that is a rounding error, but the mechanism is interesting.

Build with the CMake option BOOST_USE_MODULES=1 and existing boost/type_index includes implicitly do import boost.type_index. Your source keeps saying include. The header forwards to the module.

That turns a source migration into a build flag experiment. Turn it on, measure, turn it off if it disappoints.

Boost is not overselling it: the docs say support is early and that flags and behaviour may change.

https://wrocpp.github.io/posts/boost-modules-1-92/

## Hashtags
#cpp #cplusplus #boost #cpp20 #modules

## Alt-text
A wro.cpp social card reading "Your includes become imports", about Boost 1.92 adding C++20 module support to six libraries.

## Suggested post time
Sunday 2026-10-26, 11:00 CET
Reason: Weekend late morning for a build systems read.
