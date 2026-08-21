# Naming a constant makes GCC doubt it

## Body
This compiles on GCC 16.1:

  template for (constexpr auto m : std::define_static_array(
                    std::meta::nonstatic_data_members_of(^^T, ctx))) { ... }

This does not:

  constexpr auto members = std::define_static_array(
      std::meta::nonstatic_data_members_of(^^T, ctx));
  template for (constexpr auto m : members) { ... }

  error: 'members' is not a constant

Same expression, same initializer, same constexpr. The only difference is that the second one has a name. clang accepts both.

Worth knowing rather than filing away, because the named form is the one people write. You compute the member list once, give it a name that says what it is, and use it. Splitting a long expression out of a loop header is ordinary style, and here it turns a working program into a compile error with a message that sounds like your code is wrong.

The workaround is unpleasant in proportion: inline the expression back into the loop header, which is exactly the edit a reviewer would ask you to undo.

If you are porting reflection code written against clang, this is the shape of breakage to expect. It is not that GCC lacks the feature; it is that GCC disagrees about when a constexpr variable is usable as an expansion range.

One note on the reproducer, because my first draft was wrong in a way worth repeating. I wrote #if FORM == named to switch between the two forms. Undefined identifiers evaluate to 0 in a preprocessor condition, so that compares 0 with 0 whichever way you set it and both branches take the same path. Ask whether a macro is defined instead of comparing it to a bare word.

Reduced case, both compilers: https://wrocpp.github.io/posts/gcc-expansion-named-range/

## Hashtags
#cpp #cplusplus #cpp26 #gcc #compilers #reflection

## Alt-text
A wro.cpp card reading "Naming a constant makes GCC doubt it", about a GCC expansion statement limitation.

## Suggested post time
Wednesday 2026-10-21, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
