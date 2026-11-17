# Owning FFmpeg's libav objects, and what a missed free costs

## Body
Piotr Borys wrote on LinkedIn about RAII wrappers for FFmpeg contexts, frames and packets, so early returns and exceptions leak nothing. I measured that claim on FFmpeg 9.0.2.

FFmpeg's free functions take a pointer to the pointer and null it, so a unique_ptr needs a three-line deleter that passes &p. Each wrapper is sizeof(T*), and a static_assert checks it.

In an early-exit pipeline with manual cleanup, I forgot one free per exit. Under leaks on macOS the three early exits leaked 112 bytes, 448 bytes, and 33 allocations of 64,720 bytes. The wrapped version leaked nothing on any path.

My first run reported zero leaks for the largest case, because a stale pointer in a dead stack frame kept the context reachable. A clean leak checker means no leak it can prove. I have not read Borys's article, and this post covers allocation and free, not reference counting.

https://wrocpp.github.io/posts/raii-ffmpeg-libav/

## Hashtags
#cpp #raii #ffmpeg #memory #smartpointers #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One missed free leaked 33 allocations" with a subtitle about FFmpeg 9.0.2, 64,720 bytes and unique_ptr wrappers. Citation footer: wro.cpp, 2026-12-13.

## Suggested post time
Sunday 2026-12-13, 08:00 UTC
Reason: the morning slot on publication day; the second of the two RAII posts.
