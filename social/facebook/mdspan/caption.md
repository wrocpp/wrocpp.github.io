# std::mdspan views one flat buffer as a matrix

## Body
C++ has always stored matrices and grids in a flat buffer and done the index math by hand: data[r * cols + c]. It is fast, and a steady source of off-by-one bugs. std::mdspan (C++23) is the standard fix: a non-owning view that wraps the buffer you already have and gives it a shape.

Storage, extents, and layout are separate pieces, so one std::vector becomes a 3x4 matrix with real m[r, c] indexing and no copy. The demo runs it on GCC 16.1, which ships mdspan today. It is also the type the numerical standard library is being built around, the subject of Mark Hoemmen's fresh C++Now 2026 keynote.

https://wrocpp.github.io/posts/mdspan/

## Hashtags
#cpp #cplusplus #cpp23 #hpc #programming

## Alt-text
A cream wro.cpp social card reading "One std::vector, viewed as a matrix", about C++23 std::mdspan.

## Suggested post time
Tuesday 2026-08-04, 10:00 CET
Reason: Tuesday mid-morning CET for the EU audience.
