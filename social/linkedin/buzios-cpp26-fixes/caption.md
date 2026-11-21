# import std; breaks ^^std::basic_string on GCC 16.2, and Buzios changed the rule

## Body
Third post of a series on the Buzios meeting. The same reflection line, ^^std::basic_string, compiles after #include <string> and fails after import std; on GCC 16.2 and on GCC trunk of 21 November, with "'^^' cannot be applied to a using-declaration".

The meeting adopted P4466R2 for the C++26 draft. It lets the reflection operator name a using-declarator when only inline or unnamed namespaces lie between it and the declaration. libstdc++'s std module exports entities that way. A GCC fork that the paper credits compiled the module form and exited 0. GCC 16.2 and GCC trunk did not.

Also in the post: none of six compilers accepts a std::string_view template parameter, the limit P3861 targets, and I could read only R0 of that paper because R1 was not public. std::define_static_string returns a pointer that works as a const char* template argument today. P4453R1 adds a scheduler allocator query for task, and neither stdexec nor Beman's execution library had it on 21 November. Core issues 3241 and 3242 reword two sentences.

Reported from Sutter's trip report and the cplusplus/draft motion issues. A second DIS ballot is planned and has no date.

https://wrocpp.github.io/posts/buzios-cpp26-fixes/

## Hashtags
#cpp #cpp26 #reflection #modules #wg21 #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Reflection rejects basic_string after import std;" with a subtitle about GCC 16.2, GCC trunk and a GCC fork. Citation footer: wro.cpp, 2026-11-24.

## Suggested post time
Tuesday 2026-11-24, 16:00 UTC
Reason: second post of the day, beside the 08:00 UTC post; the four Buzios posts run one a day from 22 November.
