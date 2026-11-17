# views::as_input before filter turns a reverse bug into an error

## Body
A filter, a reverse and as_rvalue over a vector of strings compile on GCC 16.2 and overflow the heap.

I took the case from P3725R3 by Nicolai Josuttis: move the long names out of a vector of four strings, in reverse order. With -fsanitize=address, GCC 16.2 and GCC trunk of 2026-11-17 report a heap-buffer-overflow inside the filter's predicate. My reading is that the predicate runs again on strings that as_rvalue already moved from. The paper calls the program undefined behavior.

Put views::as_input before the filter and the same pipeline stops compiling at the reverse. A filter over as_input is an input range and not a forward range, and reverse needs a bidirectional one. A filter over a std::generator has the same limit. The cost is that the filtered view is single pass.

The name moves: libstdc++ 15 calls the adaptor to_input, libstdc++ 16.2 calls it as_input, and libc++ trunk had neither on Compiler Explorer. I did not check where P3725 stands in the process.

https://wrocpp.github.io/posts/views-as-input-before-filter/

## Hashtags
#cpp #cpp26 #ranges #views #undefinedbehavior #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "One adaptor turns a filter bug into a compile error" with a subtitle about filter, reverse and as_rvalue overflowing the heap on GCC 16.2 and views::as_input making the reverse a compile error. Citation footer: wro.cpp, 2026-11-26.

## Suggested post time
Thursday 2026-11-26, 08:00 UTC
Reason: the morning slot on the publication day.
