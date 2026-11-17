# A clang-tidy hook exits 2 on a header seeded with 3 history comments

## Body
Episode 9 of 9 in the tidy-agent series on clang-tidy checks for the mistakes AI coding agents keep making.

The Claude Code plugin has a PostToolUse hook that runs clang-tidy on the file the agent just edited. I ran its script by hand on a header with three comments that point at git or narrate history. With wrocpp-* in WarningsAsErrors it printed all 3 lines and exited 2. With an empty list it exited 0 and handed the same 3 lines back as context. I did not install the plugin and I did not run Claude Code itself.

The post also covers the mistake-to-check skill and its five-rung ladder, and it tables the nine checks with one number each from the earlier episodes. One spec figure turned out to describe headers, not tests, so that cell uses the count from episode 5. One log defect is reported too: in blocking mode every finding is written twice. The tenth check, public-function-contracts, is still blocked.

https://wrocpp.github.io/posts/tidy-agent-hook-and-skill/

## Hashtags
#cpp #clangtidy #aiagents #claudecode #tidyagent #staticanalysis #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A hook that exits 2 on three comments" with a subtitle about the last tidy-agent episode, a table of nine checks and what is still blocked. Citation footer: wro.cpp, 2026-12-09.

## Suggested post time
Wednesday 2026-12-09, 08:00 UTC
Reason: the morning slot on the publication day; episode 9 of 9 in the tidy-agent series.
