# C++29 mode is open, and the compilers already disagree

## Body
C++26 was finished in March. The next one is now something you can compile against.

LLVM 23.1.0 shipped on 25 August with std=c++2d, and GCC's development branch has the same mode. Neither current release will take the flag: clang 22.1 and GCC 16.2 both refuse it at the driver, before they ever look at your file.

Four lines are enough to see where each compiler thinks it is. Print __cplusplus.

Both trunks in the new mode print 202700. Two independent implementations picked the same placeholder for a standard that does not exist yet. The convention is year and month of ratification, so 202700 is not a date anyone is committing to. It sorts after everything shipped and will be replaced by a real value later.

Ask the same compilers about C++26 and the answer splits. GCC reports 202603. Clang reports 202400.

202603 is the correct one. C++26 was completed in March 2026, and the macro is year and month, so 202603 is what GCC's documentation specifies. 202400 is the placeholder clang used while the standard was in progress and has not yet updated.

That is a small thing which behaves like a large one. Feature test macros are the better tool, but a great deal of existing code tests __cplusplus directly. A comparison written against the ratified value silently takes the wrong branch on clang, because 202400 is less than 202603 even though clang is in its C++26 mode.

Even the flag spelling differs. GCC accepts std=c++29 and std=c++2d. Clang accepts only the letter form and rejects the numeric one outright.

Turning the mode on hands you no features. It opens a bucket for papers voted in after C++26, and that bucket has only just started filling.

https://wrocpp.github.io/posts/cpp29-mode-is-open/

Does your build still branch on __cplusplus anywhere?

## Hashtags
#cpp #cplusplus #cpp26 #cpp29 #clang

## Alt-text
A wro.cpp social card reading "The compilers disagree about C++26", about __cplusplus reporting 202603 on GCC and 202400 on clang.

## Suggested post time
Wednesday 2026-09-02, 09:00 CET
Reason: Weekday morning for a standards and conformance read.
