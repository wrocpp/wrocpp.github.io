# Stroustrup wants C++26 contracts pulled

## Body
The pre-Buzios mailing is out: 48 papers, and roughly a dozen of them are the same argument.

Bjarne Stroustrup, J-Daniel Garcia, Vinnie Falco, John Spicer and Ville Voutilainen have a paper titled "P2900 Contracts' fundamental flaws". It calls the C++26 contracts design an existential threat to C++ and asks for it to be replaced before the final ballot. Four companion papers push the same way: contracts are the wrong tool for undefined behaviour checks, the two should be decoupled, a smaller library based design already exists, and C++26 should go back for evaluation.

Two numbers keep that in proportion, and both come from the papers themselves.

The committee has already voted on removal. The result was SF:9 F:8 N:3 A:19 SA:41, recorded as consensus against removing contracts. Not a narrow outcome.

And the undefined behaviour framework has support rather than opposition: EWG approved the direction of P3100 at SF:16 F:15 N:6 A:2 SA:0. Zero strongly against.

So the story is not that contracts are collapsing. It is that a group including the language's designer lost that vote and is making the case again before the final ballot, partly on substance and partly on process. As P4334 puts it, a numeric rule does not weigh the implementation responsibility behind a sustained objection.

One distinction the papers blur and worth keeping straight: P2900 contracts are in the C++26 draft now, while P3100's UB framework targets C++29 and was deferred. Two arguments wearing one coat.

Also in the mailing: profiles keep moving, Barry Revzin has a paper on customising std::meta::reflect_constant, do expressions reach R5, and the usual crop of ranges additions.

The papers, the polls and what is actually at stake: https://wrocpp.github.io/posts/wg21-2026-08-mailing/

## Hashtags
#cpp #cplusplus #cpp26 #wg21 #standards #softwareengineering

## Alt-text
A wro.cpp card reading "Stroustrup wants C++26 contracts pulled", about the August 2026 WG21 mailing.

## Suggested post time
Friday 2026-08-21, 14:00 CET
Reason: midday CET catches the EU afternoon and the US morning.
