# Ship the C++20 feature and its fallback in one file

## Body
std::osyncstream is C++20, but not every compiler has it. The portable answer, straight from the code review that started this series: detect and fall back.

Include <version>, then use osyncstream if __cpp_lib_syncbuf is defined, else a static mutex. One source, the best available tool on each compiler.

Do not gate on __cplusplus: a compiler can be in C++20 mode and still lack a library feature. The per-feature macro asks the precise question.

Episode 6 of a series on concurrent I/O.

https://wrocpp.github.io/posts/feature-test-fallback/

## Hashtags
#cpp #cplusplus #cpp20 #programming #portability
