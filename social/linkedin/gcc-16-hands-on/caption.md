# GCC 16.1 ships C++26 reflection -- your 30-line hands-on

## Body
Yesterday Barry Revzin opens C++Now with reflection. Today GCC 16.1 ships it. Here is the 25-line program you can run on your laptop tonight.

The C++26 working draft was frozen at Croydon on 28 March 2026. GCC 16.1 dropped on 30 April 2026 with `-freflection`. Five weeks from "the standard is done" to "your distro's default compiler builds it." That is the fastest a C++ standard feature has ever reached a stable mainstream toolchain.

The program is the smallest hands-on we could write that proves it. Reflect a struct with `^^User`. Ask for `nonstatic_data_members_of`. Print the names. Twenty-five lines, two includes, no macros, no Boost.Hana.

```
sudo apt install gcc-16
g++-16 -std=c++26 -freflection hello_reflect.cpp -o hello
./hello
```

If you don't want to install anything, the post has a one-click Compiler Explorer link for both clang-p2996 and GCC 16.1. Identical output on both compilers.

If this is your first taste of reflection and you want to understand the primitives -- and what you can build on top of them -- the post is also the on-ramp to our 25-post series teaching reflection from the ground up.

Read it: https://wrocpp.github.io/posts/gcc-16-hands-on/

What are you reaching for first now that reflection is real?

## Hashtags
#cpp #cpp26 #reflection #gcc #p2996 #moderncpp #wrocpp

## Alt-text
Cream paper card with the wro.cpp magnet logo top-left. Headline reads "GCC 16.1 ships C++26 reflection." with the plus signs in orange and a blue period. Subtitle: released 30 April 2026 with -freflection, five weeks after the standard froze at Croydon, with a 25-line program you can run today.

## Suggested post time
Monday 2026-05-04, 10:00 CET
Reason: matches the post's pubDate so the link goes live the same morning the teaser lands; Monday morning catches European C++ engineers fresh into the week with a feel-good news peg.
