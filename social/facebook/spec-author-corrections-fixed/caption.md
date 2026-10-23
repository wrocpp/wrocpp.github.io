# Two problems confirmed by the spec's author, fixed in both bindings

## Body
The author of the Qt container spec confirmed two problems in it. I had called one a trade-off. It was a mistake, and both generated versions now announce a batch removal while the rows can still be read.

The other was a row lookup that rebuilt itself after every change. A hash drain at 10,000 entries went from 193 microseconds per removal to 320 nanoseconds.

https://wrocpp.github.io/posts/spec-author-corrections-fixed/

## Hashtags
#cpp #qt #testing #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "193 microseconds became 320 nanoseconds" with a subtitle about two problems confirmed by the spec's author. Citation footer: wro.cpp, 2026-10-26.

## Suggested post time
Monday 2026-10-26, 08:00 UTC
Reason: the morning slot, taken from the GoogleTest short, so the Qt models thread keeps moving while the spec author's answer is fresh.
