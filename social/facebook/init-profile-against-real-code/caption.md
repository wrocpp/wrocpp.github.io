# What the initialization profile says about code it was not written for

## Body
I ran the examples of P4222R3, the initialization profile, on the two experimental builds on Compiler Explorer. Both reject the paper's wrong examples and accept the right ones.

I also tried a std::jthread member declared before the counter it increments. Both builds accept it without a message. The paper does not claim the profile covers it. These are research compilers, not shipping ones.

https://wrocpp.github.io/posts/init-profile-against-real-code/

## Hashtags
#cpp #wg21 #profiles #safety #initialization #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "The init profile accepts a thread before its counter" with a subtitle about running the P4222R3 examples on two experimental builds. Citation footer: wro.cpp, 2026-11-13.

## Suggested post time
Friday 2026-11-13, 16:00 UTC
Reason: the second slot of the day.
