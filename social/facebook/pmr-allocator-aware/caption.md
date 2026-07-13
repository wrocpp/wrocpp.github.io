# Making your own type allocator-aware needs a second constructor

## Body
Put a pmr::string inside your own struct and it will allocate from the default heap, even if the struct lives in an arena, unless the struct is allocator-aware.

That means three things: an allocator_type, an optional allocator argument in each constructor, and forwarding it to the members. In the demo a Record holds a pmr::string and grows a second, allocator-extended constructor. That is what lets a pmr::vector<Record> put every nested string in the same arena, through uses-allocator construction.

The standard containers pay this tax for you. Your own types have to opt in.

Episode 7 of the pmr series.

https://wrocpp.github.io/posts/pmr-allocator-aware/

## Hashtags
#cpp #cplusplus #cpp17 #memory #programming
