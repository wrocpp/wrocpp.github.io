# Your config file, parsed at compile time

## Body
embed puts a file into the translation unit. Reflection enumerates a struct's fields. Together they parse a config file while the compiler is running.

The trick is identifier_of: the member's own name, available as a compile-time string, used as the lookup key. So the struct is the only place the schema is written, and adding a field needs no parser change.

The result is a constant, so the checks are static_asserts. Delete a line from the config and the build fails, rather than the service failing to start in an environment where the file differs from the one you tested.

Works on released GCC 16.1 with -freflection.

Runnable: https://wrocpp.github.io/posts/embed-reflect-config/

## Hashtags
#cpp #cplusplus #cpp26 #programming

## Alt-text
A wro.cpp card about parsing a config file at compile time.

## Suggested post time
Saturday 2026-10-17, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
