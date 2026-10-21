# Regenerating a Qt container library from a spec, with and without moc

## Body
Leonardo Rossi wrote the design of his observable Qt containers down as a spec an AI agent can regenerate the library from, and asked where an agent trips. I gave two fresh agents only that spec. One built it with classic moc, one with typed signals through reflect-moc, and both pass all 17 acceptance entries.

The moc version also builds with MSVC at /W4, which is the toolchain his team uses. The agents found 15 places where the spec leaves a choice and seven that look wrong, and one of them is a lazy row map that costs 193 microseconds per removal at 10,000 entries. Per entry, typed signals are 16 to 42 percent faster. The two trees were written by two agents, so the batch and reset rows are not a controlled comparison.

https://wrocpp.github.io/posts/regenerate-qt-containers-from-a-spec/

## Hashtags
#cpp #cpp26 #qt #reflection #moc #msvc #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "Two agents rebuilt a Qt library from a reader's spec" with a subtitle about one build with moc and one with typed signals, both passing 17 of 17 tests. Citation footer: wro.cpp, 2026-10-22.

## Suggested post time
Thursday 2026-10-22, 18:00 CEST (16:00 UTC)
Reason: the second post of the day, in the planned-double slot of scripts/schedule_doubles.py, to keep the discussion with the reader going.
