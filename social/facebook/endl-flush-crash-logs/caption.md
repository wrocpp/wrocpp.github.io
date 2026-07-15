# std::endl is a hidden flush, and clang-tidy flags it

## Body
std::endl is not a fancy newline. It is a newline plus a flush, and the flush costs you. A flush-counting streambuf makes it concrete: five newline-terminated lines flush zero times, five std::endl lines flush five.

Sometimes you want the flush, because it is what makes a log survive a crash (that is why std::cerr flushes every line). But on a hot path, a plain newline plus a deliberate flush at checkpoints is far cheaper. clang-tidy even ships a check, performance-avoid-endl.

Episode 7 of a series on concurrent I/O.

https://wrocpp.github.io/posts/endl-flush-crash-logs/

## Hashtags
#cpp #cplusplus #performance #programming #cleancode
