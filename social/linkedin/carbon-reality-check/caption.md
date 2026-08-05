# Carbon is still pre-0.1, with 1.0 somewhere after 2028

## Body
Carbon comes up whenever C++ succession is discussed, usually framed as a choice a team might make. Worth restating what the project itself says about its maturity, because the project is more careful about this than the discussion around it.

Carbon has not reached 0.1. The roadmap puts 0.1 at late 2026 at the earliest, with 1.0 sometime after 2028. The repository still describes it as an experiment that may not succeed. There is no stable specification, no ABI commitment, and no promise that today's syntax survives. That is not a criticism, it is a project being honest about its stage.

Its premise is narrower than "a better C++", and the narrowness is the interesting part. It targets the case where you have millions of lines of C++ that cannot be rewritten and cannot be frozen either. Rust's C++ interop, though improving, still runs through a C-shaped boundary, so templates, overloads, inheritance and exceptions do not cross cleanly. Carbon's answer is to accept C++'s object model and give up source compatibility instead, aiming for interop where C++ templates and classes are usable without wrappers.

Three positions worth holding: it is not an option for a decision you are making now; the interop work is worth watching regardless, because every successor faces that same question; and the realistic near-term answers remain C++ hardening plus selective Rust, which is exactly what Chrome published last month.

https://wrocpp.github.io/posts/carbon-reality-check/

## Hashtags
#cpp #cplusplus #carbon #programminglanguages #softwareengineering

## Alt-text
A cream wro.cpp social card reading "Carbon has not reached version 0.1", about the Carbon roadmap.

## Suggested post time
Friday 2026-08-14, 10:00 CET
Reason: mid-morning CET on the post's pubDate.
