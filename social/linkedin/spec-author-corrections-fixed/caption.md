# Two problems confirmed by the spec's author, fixed in both bindings

## Body
The author of the container spec wrote back: section 8.3 is a mistake in the spec, not a trade-off, and the lazy row map is in the real code too.

I had called the first one a trade-off because the spec says so. A batch removal erased the entries before it announced the rows, so a view reading a row in rowsAboutToBeRemoved saw nothing. Both generated bindings now announce first.

The second fix has the number. The list model rebuilt its key-to-row map after every change. A row is now found by binary search, and a hash drain at 10,000 entries went from 193 microseconds per removal to 320 nanoseconds. Each change has a test that fails on the old code.

https://wrocpp.github.io/posts/spec-author-corrections-fixed/

## Hashtags
#cpp #qt #testing #modelview #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "193 microseconds became 320 nanoseconds" with a subtitle about two problems confirmed by the spec's author. Citation footer: wro.cpp, 2026-10-26.

## Suggested post time
Monday 2026-10-26, 08:00 UTC
Reason: the morning slot, taken from the GoogleTest short, so the Qt models thread keeps moving while the spec author's answer is fresh.
