# EDG's C++ front end is open source

## Body
On 30 September the source of the EDG C++ front end went public at github.com/edgcpp/compiler. The LICENSE.txt in the repository is the LLVM project's file: Apache 2.0 with the LLVM exceptions. The C++ Alliance is the nonprofit sponsor, the way Boost operates, and John Spicer chairs the committee overseeing it. GCC, clang and EDG are now all C++ front ends whose source you can read.

The same day Compiler Explorer added EDG 7.0 and trunk builds with P2996 reflection switched on. I ran one snippet that lists a struct's data members and their types on four builds: GCC 16.2, EDG 7.0, EDG trunk and clang-p2996. All four compile and run it, and the output matches except for one spelling: GCC prints "const char*", the other three print "const char *". A test that compares display_string_of to a literal will not move between compilers.

My first draft used template for. EDG rejects it, because its builds do not define __cpp_expansion_statements, so the snippet walks the members with an index_sequence instead. GCC 16.2 and clang-p2996 accept both forms.

What is not known: how complete EDG's reflection is, since I ran one snippet. The announcement says roadmap details will be shared when they are finalized, so the release schedule is open, and so is what happens to products built on EDG.

https://wrocpp.github.io/posts/edg-front-end-open-source/

## Hashtags
#cpp #cplusplus #cpp26 #reflection #compilers #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "EDG's C++ front end is open source" with a subtitle saying that one reflection snippet ran on four builds and that EDG rejects template for. Citation footer: wro.cpp, 2026-10-08.

## Suggested post time
Thursday 2026-10-08, 18:00 CEST (16:00 UTC)
Reason: the planned second slot of the day (see schedule_doubles.py), after the evergreen post at 08:00 UTC.
