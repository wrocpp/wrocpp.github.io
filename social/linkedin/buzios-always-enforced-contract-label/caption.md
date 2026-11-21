# A contract assertion labelled enforced still terminates under ignore

## Body
P4451R2, adopted at the Buzios meeting, adds a label that makes one contract assertion terminate whatever the build asks for.

I put six assertions in one function, three of them labelled with std::contracts::controls::enforced, and built it on the GCC and Clang branch builds on Compiler Explorer. In the default call, observe ran six predicates and ignore ran three: the labelled ones. A violated labelled assertion ended the program in 12 of 12 runs, under both semantics. The same program without labels on GCC 16.2, built with -fcontracts and ignore, evaluated no predicate and exited 0.

None of the other compilers I ran has the syntax: GCC 16.2, GCC trunk, Clang 23.1 and MSVC 19.51 all failed on the file. The EDG branch built it in its P3400 mode and enforced nothing. The name differs between papers too: P3400R5, aimed at C++29, spells the label terminating.

Per Sutter's trip report, the committee adopted it in response to national body comments. I take no side in the dispute. The post has the paper's rules by section, the compiler table and every run.

https://wrocpp.github.io/posts/buzios-always-enforced-contract-label/

## Hashtags
#cpp #cpp26 #contracts #wg21 #buzios #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A contract check the build cannot ignore" with a subtitle about P4451R2, 3 of 6 predicates under ignore and 12 of 12 terminating runs. Citation footer: wro.cpp, 2026-11-23.

## Suggested post time
Monday 2026-11-23, 16:00 UTC
Reason: the second post of the day; the four Buzios posts run at 16:00 UTC from 22 November.
