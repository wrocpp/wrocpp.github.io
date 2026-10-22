# 228 Qt model edge cases, and the ones my models failed

## Body
I wrote down 228 edge cases for the observable Qt models and tested each one against Qt's own models. 170 work, 22 are refused on purpose, 20 were defects that now have a fix and a test, and 16 are still pinned by a test that passes while the gap exists.

The defects were in my own code: an editor that can write an empty value back, a removal that reads empty rows, a model that keeps stale rows when its container dies, and a nested change from a receiver that crashed 10 of 100 list cases. Nothing is merged yet: four pull requests are open and a few fixes are still being written.

https://wrocpp.github.io/posts/qt-model-edge-cases-catalogue/

## Hashtags
#cpp #qt #testing #modelview #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "228 Qt model edge cases, tested" with a subtitle about 170 cases that work, 20 defects fixed and 16 still pinned. Citation footer: wro.cpp, 2026-10-22.

## Suggested post time
Thursday 2026-10-22, 10:00 CEST (08:00 UTC)
Reason: the morning slot, taken from the evergreen post that moved to 23 October, so the discussion on the Qt models keeps moving.
