# A stepping debugger is a coroutine that stops at checkpoints

## Body
Alexey Ozeritskiy wrote on LinkedIn about a debugger for WebAssembly built on coroutines. The project is Qumir, and its design notes are public. The compiler emits a checkpoint before each statement. Most checkpoints do nothing and return at once. A stopping one suspends the program and hands control back to the browser.

I modelled that mechanism in a C++20 program under 200 lines: breakpoints, step into, over and out, a call stack, and a fast path that never suspends. On GCC 16.2 a run with no breakpoints evaluated 14 checkpoints and stopped at none. Stepping over a call ran the function with no stop inside it.

It is a toy and not their code. It runs natively, has no variables or user interface, and I did not run Qumir. The next post measures what a coroutine per call costs.

https://wrocpp.github.io/posts/coroutine-single-stepper/

## Hashtags
#cpp #cpp20 #coroutines #debugging #webassembly #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A debugger built from coroutine suspend points" with a subtitle about a WebAssembly debugger on coroutines and a C++20 toy under 200 lines. Citation footer: wro.cpp, 2026-12-10.

## Suggested post time
Thursday 2026-12-10, 08:00 UTC
Reason: the morning single on publication day, beside the structured-binding short that runs at 16:00 UTC.
