# std::array became compile-time in pieces, and the algorithms went last

## Body
C++11 gave std::array a constexpr constructor. C++14 added more members. C++17 finished the container. And C++20 finished the algorithms, which is the step that actually mattered: std::sort, std::iota and most of <algorithm> only became constexpr then.

That gap is why so much older lookup-table code contains a hand-written compile-time bubble sort. Between C++17 and C++20 you could build an array at compile time but not sort it with the standard library.

The demo builds an array, squares every element and sorts it descending, entirely during compilation. The static_asserts are the proof: if any of it escaped to runtime the program would not compile.

Useful for tables you would otherwise generate with a script, and they reach the binary as constant data with no startup cost.

https://wrocpp.github.io/posts/constexpr-array-evolution/

## Hashtags
#cpp #cplusplus #constexpr #cpp20 #programming

## Alt-text
A cream wro.cpp social card reading "Sorting at compile time waited for C++20", about the constexpr evolution of std::array.

## Suggested post time
Wednesday 2026-08-19, 10:00 CET
Reason: midweek mid-morning CET for the EU audience.
