# Generating an RPC client and a mock as callable data members

## Body
This class has no add() function, and client.add(2, 3) still works. C++26 reflection can only add data members to a generated class, so each method of an interface becomes an empty data member with an operator(). That gives an RPC client with no IDL and a mock for generic code. The client is 32 bytes on GCC 16.2.

The post lists what does not work: overloads, const methods, and passing the mock where a virtual reference is required.

https://wrocpp.github.io/posts/generate-rpc-client-and-mock-with-data-members/

## Hashtags
#cpp #cpp26 #reflection #rpc #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "This class has no add(), and client.add(2, 3) works" with a subtitle saying that a data member with an operator() gives C++26 an RPC client and a mock, and that the client is 32 bytes. Citation footer: wro.cpp, 2026-11-10.

## Suggested post time
Tuesday 2026-11-10, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
