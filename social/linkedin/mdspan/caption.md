# std::mdspan views one flat buffer as a matrix

## Body
C++ programs have always stored matrices, images, and grids in a flat buffer and done the index math by hand: data[r * cols + c]. It works, it is fast, and it is a steady source of off-by-one and row-versus-column bugs. std::mdspan (C++23) is the standard fix: a non-owning view that wraps the flat buffer you already have and gives it a shape.

The design is three separable pieces. Storage is your contiguous array, owned by whatever already owns it. Extents are the shape, any mix of compile-time and runtime dimensions. A layout maps indices to offsets, row-major by default, with column-major and strided built in. mdspan owns none of the data and adds no allocation. It is span with more than one dimension.

The demo views a std::vector of twelve elements as three rows of four, indexed with the real C++23 multidimensional subscript m[r, c]. No copy, and the vector still owns its storage.

That is why it matters beyond convenience: mdspan is the type the numerical parts of the standard library are built around, the way you hand a tensor slice to a BLAS-style routine without committing to a container. Mark Hoemmen's C++Now 2026 keynote is on exactly that direction, and GCC 16.1 ships mdspan today: https://wrocpp.github.io/posts/mdspan/

Where in your code are you still doing r * cols + c by hand?

## Hashtags
#cpp #cplusplus #cpp23 #mdspan #hpc #performance #programming

## Alt-text
A cream wro.cpp social card reading "One std::vector, viewed as a matrix", about C++23 std::mdspan as a non-owning multidimensional view.

## Suggested post time
Tuesday 2026-08-04, 10:00 CET
Reason: Tuesday mid-morning CET, a strong weekday slot for the EU C++ audience.
