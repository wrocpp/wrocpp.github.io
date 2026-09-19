# 228 of 2,613 tracked C++ projects now ship a module

## Body
The arewemodulesyet tracker counts 228 projects with a C++20 module. Its own recorded history has 2 in April 2024 and 62 in November 2025, so the curve is steep.

The number sitting next to it is 2,613. That is how many projects the tracker follows, which puts adoption at 8.7 percent.

A tick on that tracker means a module exists. It does not mean the module is on. I checked three well-known entries. FTXUI keeps its module behind FTXUI_BUILD_MODULES, off by default. nlohmann/json needs NLOHMANN_JSON_BUILD_MODULES and its own documentation calls the module experimental, with exported symbols that may still change. fmt 12.2.0 enables FMT_MODULE only when CMake is 3.28 or newer, the standard is C++20 or later, and the generator is Ninja or Visual Studio. Configure it the way most projects do, with Makefiles, and you get headers.

Underneath the libraries sits import std. In a single file on Compiler Explorer it builds on GCC 16, and only when GCC is told to compile the std module itself. Clang 20.1 reports that module std was not found, and MSVC reports C2230. Neither is missing the feature. Both expect the build system to compile the std module first, and GCC moved that step into the compiler.

Every compiler row in the post was measured on Compiler Explorer rather than quoted from documentation.

https://wrocpp.github.io/posts/modules-tracker-228/

Which library would you most want to import instead of include?

## Hashtags
#cpp #cpp20 #modules #importstd #cmake #moderncpp #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "228 libraries ship a C++ module. That is 8.7%." with a subtitle noting the tracker follows 2,613 projects and that a tick means the module exists, not that it is switched on. Citation footer: wro.cpp, 2026-09-21.

## Suggested post time
Monday 2026-09-21, 18:00 CET (16:00 UTC)
Reason: matches the post's own 16:00Z slot, so the card and the link go out together and the page is live when the post lands. Monday evening CET also catches US morning.
