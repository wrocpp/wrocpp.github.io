# Of the 14 C++29 motions from Buzios, two already run on a compiler

## Body
Fourth post in a series on the Buzios meeting.

The committee adopted 14 motions for the C++29 draft: 11 papers and 3 lists of issues. I tried the code of seven of the papers on Compiler Explorer on 21 November.

Two already run. The 0o octal prefix is accepted by Clang 23.1 and trunk, where 0o17 is 15. std::clmul and std::widening_clmul are in libstdc++ on GCC trunk, in the C++29 mode only (-std=c++2d). Labelled break and continue run in C with every compiler I tried. In C++ they run on Clang behind -Xclang -fnamed-loops, which still rejects a reused label.

Four have nothing to run: views::slice, any_view, get_ptr on optional, and auto return types on defaulted operators. For each I wrote the equivalent that compiles today, and the post lists the compilers and flags that missed them.

The count comes from the motion issues in the C++ draft repository. Sutter's trip report says five core and seven library papers. The issues show six library papers plus a list of library issues.

https://wrocpp.github.io/posts/buzios-cpp29-papers/

## Hashtags
#cpp #cpp29 #wg21 #cplusplus #compilers #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Two of the 14 new C++29 motions already run" with a subtitle about the 0o octal prefix, std::clmul and loop labels. Citation footer: wro.cpp, 2026-11-25.

## Suggested post time
Wednesday 2026-11-25, 08:00 UTC
Reason: the morning slot on the publication day; the fourth post of the daily series on the Buzios meeting.
