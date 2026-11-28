# std::inplace_vector is not a pimpl buffer, and C++26 trivial unions do not make one

## Body
Episode 2 of the series on pimpl and type erasure in C++26.

Yesterday's pimpl kept its Impl in an aligned byte array. Is there a standard type for that now? I measured the candidates against an Impl of 72 bytes aligned to 8.

std::inplace_vector<std::byte, 72> is 73 bytes with alignment 1 in libstdc++ 16.2. The extra byte is its element count, and it cannot hold an object that needs 8-byte alignment. libc++ trunk has no <inplace_vector> yet.

std::aligned_storage still compiles, and GCC 16.2 warns that it is deprecated.

C++26 trivial unions (P3074R7) let a union hold a std::string member without a hand-written constructor and destructor. Only GCC trunk has them on Compiler Explorer. The paper was first titled std::uninitialized<T>; the library type was dropped for the language change and is not in C++26.

None of this helps a pimpl header: a union member must be a complete type, and the header only declares Impl. The aligned byte array stays.

https://wrocpp.github.io/posts/which-std-type-can-be-a-buffer/

## Hashtags
#cpp #cpp26 #pimpl #inplacevector #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A 72-byte buffer that comes out at 73 bytes" with a subtitle about std::inplace_vector's counter and alignment and C++26 trivial unions on GCC trunk. Citation footer: wro.cpp, 2027-01-14.

## Suggested post time
Thursday 2027-01-14, 08:00 UTC
Reason: the morning slot on the publication day; the four episodes run daily, 13 to 16 January.
