# A queue for changes made during a notification, in both bindings

## Body
The author of the Qt container spec sent an addendum on one question: what happens when a receiver changes the container that is notifying it. The answer is a queue. The change waits, and the queue drains in order when the outermost notification closes.

Both generated bindings now do it. The twelve acceptance tests of the addendum fail or crash the old code in both, and pass after, in Debug and Release. Three of them pass on the old code as worded, because the recorder is connected first, so the agent added a check inside the receiver. A single change costs 3 to 31 percent more. Batches do not.

The addendum leaves the matrix out because no test shows the failure. A test now does: of 32 nested cases, 20 crash and 4 end with a model that agrees with the matrix but announced a stale index. Nothing in the matrix was changed.

https://wrocpp.github.io/posts/spec-addendum-nested-changes/

## Hashtags
#cpp #qt #testing #modelview #reflection #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "24 of 32 nested changes broke the matrix" with a subtitle about the spec addendum and the matrix test. Citation footer: wro.cpp, 2026-11-04.

## Suggested post time
Wednesday 2026-11-04, 16:00 UTC
Reason: the second slot of the day, so the Qt models thread keeps its pace while the spec author's addendum is a week old.
