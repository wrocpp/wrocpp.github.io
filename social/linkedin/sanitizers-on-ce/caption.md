# The sanitizers run live on Compiler Explorer

## Body
The sanitizers are the cheapest correctness tools in C++, and most people still file them under "things I set up locally when I have time". You do not have to. AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer all run in Compiler Explorer's execution pane.

Add one -fsanitize flag, turn on execution, and the runtime report prints in the browser. ASan gives you the faulting line, the allocation site, and the shadow-byte map for a heap overflow. UBSan names the signed-overflow line and the exact operands. TSan flags a data race with both conflicting stacks, even on a run where the counter happens to add up correctly.

That last case is the useful one. A data race is a property of the code, not of whether one execution lost a write, so TSan reports it either way. And because the whole thing is a shareable link, a sanitizer report becomes something you can send a colleague instead of describing over a call.

Three flags, three classic bugs, all running: https://wrocpp.github.io/posts/sanitizers-on-ce/

Which sanitizer has saved you the most debugging time?

## Hashtags
#cpp #cplusplus #sanitizers #debugging #asan #compilerexplorer #programming

## Alt-text
A cream wro.cpp social card reading "One flag, and the bug names its own line", about AddressSanitizer, UBSan, and ThreadSanitizer running on Compiler Explorer.

## Suggested post time
Thursday 2026-07-23, 10:00 CET
Reason: post lands on its pubDate; mid-morning CET reaches the EU C++ audience during the workday.
