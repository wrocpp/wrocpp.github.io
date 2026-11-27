# At Buzios, a poll to remove contracts from C++26 failed 41 to 90

## Body
Mateusz Pusz's report from the Buzios meeting gives a number that Herb Sutter's report did not. A poll to remove contracts from C++26 got 41 votes for, 90 against and 20 abstentions, and did not reach consensus. Contracts stay in the revised draft.

Pusz also writes that the new DIS ballot takes eight weeks. The vote to send the draft to that ballot was 111 for, 9 against, 8 abstaining, the same numbers Sutter gives. I found no start date for the ballot.

The second item is P3861R1. Per Pusz it makes string_view, span, tuple, optional and variant structural, so they can be template arguments. He disagrees with special-casing a few standard types, and the post quotes his reason. The paper itself was still not public on 28 November.

I reran the limit that day. GCC 16.2, GCC trunk and Clang trunk all reject optional, string_view and span as template parameter types. The post has a runnable workaround with small structs of your own, and four practices you can apply now, each tied to a run or a source.

https://wrocpp.github.io/posts/pusz-buzios-report-contracts-poll/

## Hashtags
#cpp #cpp26 #contracts #wg21 #iso #wrocpp

## Alt-text
wro.cpp card with the magnet logo. Headline reads "A vote to drop contracts lost 41 to 90" with a subtitle about Mateusz Pusz's Buzios report, the eight-week ballot and five standard types that become structural. Citation footer: wro.cpp, 2026-11-30.

## Suggested post time
Monday 2026-11-30, 16:00 UTC
Reason: the second post of the day, beside the 08:00 UTC post, in the slot held after the Buzios series.
