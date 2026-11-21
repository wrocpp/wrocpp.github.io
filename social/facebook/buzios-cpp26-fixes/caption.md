# import std; breaks ^^std::basic_string on GCC 16.2, and Buzios changed the rule

## Body
Third post on the Buzios meeting. On GCC 16.2 and GCC trunk, ^^std::basic_string compiles after #include and fails after import std;. The meeting adopted P4466R2 for the C++26 draft to change that, and a GCC fork accepted the module form. The post also covers string_view as a template argument, a new allocator query for task, and two core issues.

https://wrocpp.github.io/posts/buzios-cpp26-fixes/

## Hashtags
#cpp #cpp26 #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Reflection rejects basic_string after import std;" with a subtitle about GCC 16.2, GCC trunk and a GCC fork. Citation footer: wro.cpp, 2026-11-24.

## Suggested post time
Tuesday 2026-11-24, 16:00 UTC
Reason: second post of the day, beside the 08:00 UTC post; the four Buzios posts run one a day from 22 November.
