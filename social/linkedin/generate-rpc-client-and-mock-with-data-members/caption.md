# Generating an RPC client and a mock as callable data members

## Body
rpc::client<Api> has no member function called add. It has a data member called add, and that member has an operator(), so client.add(2, 3) serializes the arguments, sends them through a transport and reads an int back.

C++26 reflection can synthesize a class with define_aggregate, but only with data members. One empty member per method of an interface gives an RPC client with no IDL and, with state in each member, a Mock<IClock> for code that is generic over its clock. Each member finds its owner as this minus offset_of(member). With [[no_unique_address]] the client is 32 bytes, the size of its transport, against 40 without the attribute.

The limits are in the post with the GCC 16.2 error texts: overloaded methods are refused, const and noexcept methods are refused, and the mock cannot be passed where a virtual IClock& is required. It was tested on GCC 16.2 only, and the demos run on Compiler Explorer.

https://wrocpp.github.io/posts/generate-rpc-client-and-mock-with-data-members/

This is the replacement that the correction in the auto-mocks post promised: https://wrocpp.github.io/posts/auto-mocks/

## Hashtags
#cpp #cpp26 #reflection #rpc #mocking #wrocpp

## Alt-text
Dark wro.cpp card with the magnet logo. Headline reads "This class has no add(), and client.add(2, 3) works" with a subtitle saying that a data member with an operator() gives C++26 an RPC client and a mock, and that the client is 32 bytes. Citation footer: wro.cpp, 2026-11-10.

## Suggested post time
Tuesday 2026-11-10, 08:00 UTC (09:00 CET)
Reason: a single flagship post for the day.
