# Your config file, parsed at compile time

## Body
Two C++26 features that are individually neat and jointly useful. embed pulls a file into the translation unit as data. Reflection enumerates a type's members. Together they turn a configuration file into a compile-time constant.

The usual version writes every key twice, once in the struct and once in the parser. Reflection gets the names from the members themselves, so the struct is the only place the schema is written:

  ((out.[:members[I]:] = lookup(text, std::meta::identifier_of(members[I]))), ...);

identifier_of is what makes it work: the member's own name, available as a compile-time string, used as the lookup key. Add a field and it is looked up without touching the parser.

Because the whole thing runs during translation, the result is a constant and the checks are assertions. Delete a line from the config file and the build fails with your message. The alternative, which most programs still do, is to discover it when the service will not start, in an environment where the file is different from the one you tested with.

That is the real argument. Not speed, though there is no parsing at run time, and not elegance. A configuration error becomes a compile error, and compile errors happen to the person who made them.

Both halves work on a released compiler, which surprised me: GCC 16.1 takes this with -freflection and the standard meta header.

Where it stops: this only applies to configuration genuinely fixed at build time. A file the operator edits after deployment is not this. Feature flags, embedded schemas, route tables, build-stamped defaults are.

Runnable: https://wrocpp.github.io/posts/embed-reflect-config/

## Hashtags
#cpp #cplusplus #cpp26 #reflection #metaprogramming

## Alt-text
A wro.cpp card reading "Your config file, parsed at compile time", about combining embed with reflection.

## Suggested post time
Saturday 2026-10-17, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
