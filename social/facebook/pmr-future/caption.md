# WG21 now says new library types must ship a pmr alias

## Body
The idea that std::pmr is a dead C++17 experiment is backwards. In 2024 WG21 adopted a policy (P3002) that every new allocating standard type should ship a pmr alias, the way pmr::vector and pmr::string already do.

Two papers follow: P3153 makes optional allocator-aware, and P1083 brings resource_adaptor in C++26, a bridge from any classic allocator to a memory_resource. The demo hand-rolls that bridge and runs a pmr::vector on a classic allocator.

pmr is the runtime half of the allocator model, and the standard is being built to lean on it, not away from it.

Episode 8 of the pmr series.

https://wrocpp.github.io/posts/pmr-future/

## Hashtags
#cpp #cplusplus #cpp26 #memory #programming
