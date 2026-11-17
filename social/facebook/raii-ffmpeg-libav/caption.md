# Owning FFmpeg's libav objects, and what a missed free costs

## Body
Piotr Borys wrote about RAII wrappers for FFmpeg objects. I measured the claim on FFmpeg 9.0.2. A unique_ptr with a small deleter owns a packet, frame or codec context at the cost of one pointer. A pipeline with manual cleanup leaked at all three early exits, the largest 64,720 bytes in 33 allocations. The wrapped version leaked nothing.

https://wrocpp.github.io/posts/raii-ffmpeg-libav/

## Hashtags
#cpp #raii #ffmpeg #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One missed free leaked 33 allocations" with a subtitle about FFmpeg 9.0.2, 64,720 bytes and unique_ptr wrappers. Citation footer: wro.cpp, 2026-12-13.

## Suggested post time
Sunday 2026-12-13, 08:00 UTC
Reason: the morning slot on publication day; the second of the two RAII posts.
