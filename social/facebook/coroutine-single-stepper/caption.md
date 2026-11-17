# A stepping debugger is a coroutine that stops at checkpoints

## Body
Alexey Ozeritskiy built a WebAssembly debugger out of coroutines: a checkpoint before each statement either continues or suspends and hands control back to the host. I modelled the mechanism in a C++20 program under 200 lines. On GCC 16.2 a run with no breakpoints evaluated 14 checkpoints and stopped at none. It is a toy and not their code.

https://wrocpp.github.io/posts/coroutine-single-stepper/

## Hashtags
#cpp #coroutines #debugging #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A debugger built from coroutine suspend points" with a subtitle about a WebAssembly debugger on coroutines and a C++20 toy under 200 lines. Citation footer: wro.cpp, 2026-12-10.

## Suggested post time
Thursday 2026-12-10, 08:00 UTC
Reason: the morning single on publication day, beside the structured-binding short that runs at 16:00 UTC.
