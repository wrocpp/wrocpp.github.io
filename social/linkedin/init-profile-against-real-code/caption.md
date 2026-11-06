# What the initialization profile says about code it was not written for

## Body
I ran the examples of P4222R3, the initialization profile, on the two experimental builds on Compiler Explorer, on 2 November 2026. Both reject the paper's wrong examples and accept its right ones. They differ on a few details, such as int* p2 [[uninit]]; and std::byte x;.

I added one case from outside the paper: a std::jthread member declared before the atomic it increments. Both builds compile it with no output, and the program exits 0. Declaring the thread last gives the same output, so the profile does not tell the two orders apart. The paper does not claim to cover this, and I did not run the program under a sanitizer for this post.

These are research forks, not shipping compilers.

https://wrocpp.github.io/posts/init-profile-against-real-code/

## Hashtags
#cpp #wg21 #profiles #safety #initialization #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "The init profile accepts a thread before its counter" with a subtitle about running the P4222R3 examples on two experimental builds. Citation footer: wro.cpp, 2026-11-13.

## Suggested post time
Friday 2026-11-13, 16:00 UTC
Reason: the second slot of the day.
