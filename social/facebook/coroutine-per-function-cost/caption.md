# What it costs to make every function a coroutine

## Body
In a toy model on GCC 16.2, turning recursive Fibonacci into coroutines cost one 80-byte heap allocation per call: 635,621 calls, 635,621 allocations, against none for the plain function. A checkpoint that never stops added nothing I could tell apart from noise. At -O0, fib(22) crashed on the default stack. It is a toy, and not Qumir.

https://wrocpp.github.io/posts/coroutine-per-function-cost/

## Hashtags
#cpp #coroutines #performance #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A coroutine call costs one 80-byte allocation" with a subtitle about 635,621 calls and allocations in a toy on GCC 16.2 and a stack crash at -O0. Citation footer: wro.cpp, 2026-12-11.

## Suggested post time
Friday 2026-12-11, 08:00 UTC
Reason: the morning slot on publication day; it follows the single-stepper post from the day before.
