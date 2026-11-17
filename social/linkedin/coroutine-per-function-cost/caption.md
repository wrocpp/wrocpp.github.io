# What it costs to make every function a coroutine

## Body
A coroutine debugger needs each function that can reach a checkpoint to be a coroutine, so the cost is paid per call. I measured it in a toy model on GCC 16.2, with recursive Fibonacci as the worst case.

fib(27) makes 635,621 calls. Plain recursion made no heap allocations. The coroutine versions made 635,621, one per call, at 80 bytes each. A checkpoint that never stops added no allocation.

Time is noisy on my machine. The plain function took 0.29 to 0.49 ms in every run, and no coroutine run on the Mac was faster than about 16 ms. In the quietest runs the coroutine versions were at least 40 to 50 times the plain function, and the checkpoint's fast path cost less than the noise. My first single run said the checkpoint tripled the cost, and that was noise.

At -O0 fib(22) crashed on the default stack, while fib(20) ran. A 1 GiB stack completed it. I do not have an explanation. This is a toy, not Qumir, and I did not measure the measures its design notes describe.

https://wrocpp.github.io/posts/coroutine-per-function-cost/

## Hashtags
#cpp #cpp20 #coroutines #performance #debugging #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A coroutine call costs one 80-byte allocation" with a subtitle about 635,621 calls and allocations in a toy on GCC 16.2 and a stack crash at -O0. Citation footer: wro.cpp, 2026-12-11.

## Suggested post time
Friday 2026-12-11, 08:00 UTC
Reason: the morning slot on publication day; it follows the single-stepper post from the day before.
