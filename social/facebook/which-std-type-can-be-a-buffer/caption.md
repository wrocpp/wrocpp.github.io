# std::inplace_vector is not a pimpl buffer, and C++26 trivial unions do not make one

## Body
Episode 2 of the series on pimpl and type erasure in C++26. A std::inplace_vector of 72 bytes is 73 bytes with alignment 1 in libstdc++ 16.2, so it cannot hold a pimpl's Impl. C++26 trivial unions remove the boilerplate of a union slot, but of the compilers on Compiler Explorer only GCC trunk has them, and a union needs the complete type a pimpl header does not have.

https://wrocpp.github.io/posts/which-std-type-can-be-a-buffer/

## Hashtags
#cpp #cpp26 #pimpl #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A 72-byte buffer that comes out at 73 bytes" with a subtitle about std::inplace_vector's counter and alignment and C++26 trivial unions on GCC trunk. Citation footer: wro.cpp, 2027-01-14.

## Suggested post time
Thursday 2027-01-14, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run daily, 13 to 16 January.
