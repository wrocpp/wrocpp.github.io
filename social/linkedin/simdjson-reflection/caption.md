# simdjson meets reflection: sb << my_struct at 6.8 GB/s

## Body
simdjson now ships a C++26 reflection backend. Define SIMDJSON_STATIC_REFLECTION before including simdjson.h and sb << my_struct serializes any aggregate at SIMD speed.

The CITM Catalog benchmark hits 6.8 GB/s after a register-level optimization that keeps the write position in a CPU register across the entire inlined call chain (+45% over the previous version).

P3394 annotations coming next: [[simdjson::rename("user_name")]] and [[simdjson::skip]] for field-level customization.

The two fastest C++ JSON libraries (simdjson and Glaze) both independently chose reflection as their integration path. The API is stable enough to build on.

https://wrocpp.github.io/posts/simdjson-reflection/

## Hashtags
#cpp #cpp26 #reflection #simdjson #json #serialization #simd #p2996 #wrocpp

## Alt-text
Editorial card: "simdjson meets reflection: sb << my_struct at 6.8 GB/s". SIMD-accelerated JSON serialization via C++26 compile-time reflection.

## Suggested post time
Tuesday 2026-06-02, 10:00 CET
