# A vote is not the same as agreement

## Body
C++26 contracts are not a proposal. They are text in the working draft, voted in, implemented in GCC 16.1, and demonstrable today. The August mailing contains a paper by the designer of C++ arguing they should come out anyway.

That is unusual enough to be worth understanding properly, and it is not a story about contracts being broken. It is a story about what consensus means when a feature is nearly shipped.

The concrete objections are more interesting than the framing. Stripped to the ones that can be checked: contracts on virtual functions, capturing an object's original value for a postcondition, and the framework for core-language undefined behaviour are all deferred to C++29. No shipping production codebase uses pre, post and contract_assert. The standard libraries harden with their own assertion macros instead, at around 0.3% overhead measured across Google's fleet, and contracts are not wired into them. The set of evaluation semantics was still growing during review, with quick_enforce arriving in revision 7.

Then two numbers from the record.

The committee has already voted on removal: SF:9 F:8 N:3 A:19 SA:41, recorded as consensus against. And the UB framework was approved by EWG at SF:16 F:15 N:6 A:2 SA:0, with nobody strongly against.

So the real disagreement is procedural. The committee resolves disagreement by counting votes in five buckets. The objectors' position is that when compiler vendors sustain an objection to a foundational feature, a majority against them is evidence of a process failure rather than a settled question. The counter-position is that a vote is how a standards body decides, and losing one is not the same as being ignored.

What it means if you write C++: very little immediately, and that is worth saying clearly because standards disputes read as more alarming than they are.

Both cases, from the papers: https://wrocpp.github.io/posts/contracts-dispute/

## Hashtags
#cpp #cplusplus #cpp26 #wg21 #standards #softwareengineering

## Alt-text
A wro.cpp card reading "A vote is not the same as agreement", about the C++26 contracts dispute.

## Suggested post time
Sunday 2026-08-30, 10:00 CET
Reason: weekday mid-morning CET suits the EU C++ audience.
