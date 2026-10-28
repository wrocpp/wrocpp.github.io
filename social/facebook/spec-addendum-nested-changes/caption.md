# A queue for changes made during a notification, in both bindings

## Body
The author of the Qt container spec sent an addendum: when a receiver changes the container that is notifying it, queue the change and apply it when the outermost notification closes. Both generated bindings now do, and its twelve tests pass.

It leaves the matrix out because no test shows the failure. Now one does. Of 32 nested cases, 24 break the matrix or its model.

https://wrocpp.github.io/posts/spec-addendum-nested-changes/

## Hashtags
#cpp #qt #testing #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "24 of 32 nested changes broke the matrix" with a subtitle about the spec addendum and the matrix test. Citation footer: wro.cpp, 2026-11-04.

## Suggested post time
Wednesday 2026-11-04, 16:00 UTC
Reason: the second slot of the day, beside the contract_assert post.
