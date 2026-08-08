# std::array became compile-time in pieces, and the algorithms went last

## Body
Compile-time containers arrived in instalments, and the order confuses people who assume std::array was always fully usable in a constant expression.

C++11 gave it a constexpr constructor and element access. C++14 made more members constexpr. C++17 finished the container itself: begin, end, data, fill, swap. And C++20 finished the algorithms, which is the step that actually mattered: std::sort, std::iota, most of <algorithm> and <numeric>, plus the ranges versions.

That last step is the one worth internalising. Between C++17 and C++20 you could build a std::array at compile time but not sort it with the standard library, which is why so much older lookup-table code contains a hand-written compile-time bubble sort. Those can be deleted now.

The demo builds an array with iota, squares each element, and sorts it descending with ranges::sort, all during compilation. The static_asserts are the proof rather than decoration: if any part escaped to runtime the program would not compile.

Where it pays off is the table you would otherwise generate with a script: sorted keyword lists for a lexer, CRC or sine tables, dispatch tables sorted for binary search. Written this way the table lives in the source in readable form, is checked by the compiler, and reaches the binary as constant data with no static initialiser.

Two limits: compilers cap constant evaluation, so very large tables need the limit raised, and everything computed this way is build time you pay on every compile.

https://wrocpp.github.io/posts/constexpr-array-evolution/

## Hashtags
#cpp #cplusplus #constexpr #cpp20 #metaprogramming #programming

## Alt-text
A cream wro.cpp social card reading "Sorting at compile time waited for C++20", about the constexpr evolution of std::array.

## Suggested post time
Wednesday 2026-08-19, 10:00 CET
Reason: midweek mid-morning CET for the EU audience.
