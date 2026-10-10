"""Dates that deliberately carry two posts, and when the second one is advertised.

Shared by check-pubdates.py (which enforces the shape) and
auto-schedule-next.py (which acts on the hour), so the plan lives in one place
and the two scripts cannot drift apart.

Background. The site publishes one post a day, and auto-schedule-next.py pushes
every post to Buffer at 08:00Z. A second post sharing a date would therefore be
pushed into the same slot as the first, and one of the two would go out
unadvertised -- which is why check-pubdates.py treats a duplicate pubDate as an
error, and why it has three recorded incidents behind it.

The 08:00Z limit turns out to belong to auto-schedule-next.py, not to Buffer.
push-to-buffer.py accepts an explicit --at. So two posts can share a date as
long as the second is pushed at a different hour, which is what this table
records.

This is NOT a way to silence the duplicate-pubDate gate. Adding a date here is a
publishing decision: it says a second post is planned for that day, names the
slug it will have, and fixes the hour it goes out at. The gate checks that
reality matches, and warns while the planned post is still unwritten.
"""

# date -> {slug of the SECOND post, UTC hour it is pushed at, why}
INTENTIONAL_DOUBLES: dict[str, dict] = {
    # 14 to 18 September 2026 each reserved a second slot for a CppCon daily
    # short. None were written: the posts needed same-day reporting from the
    # conference that never arrived, so five 16:00Z slots went out empty.
    # The entries are removed because the dates have passed and a warning
    # about a date in the past trains you to ignore the gate. A daily-post
    # reservation only works if someone is committed to filing each day.
    # The modules tracker passed 228 projects on 8 September. A reactive short
    # runs alongside the reflection series post instead of waiting for the
    # first open date in November.
    "2026-09-21": {"slug": "modules-tracker-228", "hour": 16,
                   "why": "modules tracker news alongside the reflection series"},
    # The CUDA piece is the technical companion to Neil Talap's article
    # (issue #107). It moves up from 19 October so both go live the same day.
    "2026-09-26": {"slug": "cuda-lock-in-is-not-the-language", "hour": 16,
                   "why": "companion to a guest article publishing the same day"},
    # A reader's LinkedIn comment on enum aliases gets its answer while the
    # thread is still active, beside the cross-language flagship.
    "2026-10-01": {"slug": "enum-aliases", "hour": 16,
                   "why": "reply to a reader comment alongside the flagship"},
    # The Packt C++ book bundle on Humble ends on 12 October, so the short
    # runs now beside the reflection series post rather than after the sale.
    "2026-10-02": {"slug": "humble-cpp-masterclass", "hour": 16,
                   "why": "time-limited book bundle alongside the reflection series"},
    # First episode of the reflect-moc series (Qt meta-objects from C++26
    # reflection). The topic is current now, so it runs beside the evergreen
    # post of the day instead of waiting for the first open date.
    "2026-10-06": {"slug": "qt-metaobject-from-reflection", "hour": 16,
                   "why": "reflect-moc series episode 1 alongside the evergreen post"},
    # EDG's C++ front end was open-sourced on 30 September and Compiler
    # Explorer added reflection builds the same day, so the short runs
    # beside the evergreen post (pmr-allocator-aware) rather than waiting.
    "2026-10-08": {"slug": "edg-front-end-open-source", "hour": 16,
                   "why": "EDG open-source news alongside the evergreen post"},
    # Second episode of the reflect-moc series (why a Qt signal is a data member
    # and what it costs). It runs beside the evergreen post of the day.
    "2026-10-09": {"slug": "qt-signals-as-data-members", "hour": 16,
                   "why": "reflect-moc series episode 2 alongside the evergreen post"},
    # A short on the September mailing's three contracts papers, written while
    # the mailing is current, beside the evergreen ctre-costs post.
    "2026-10-10": {"slug": "dis-ballot-contracts-papers", "hour": 16,
                   "why": "mailing news short alongside the evergreen post"},
    # Third episode of the reflect-moc series (how RQT_OBJECT finds its class and
    # how RQT_PROPERTY parses the Q_PROPERTY text). It runs beside the evergreen
    # post of the day.
    "2026-10-12": {"slug": "qt-object-that-never-names-its-class", "hour": 16,
                   "why": "reflect-moc series episode 3 alongside the evergreen post"},
    # A reactive GCC trunk short on a coroutine promise with both return_value
    # and return_void (P3950R1), beside the evergreen optional-ref post.
    "2026-10-14": {"slug": "coroutine-return-void-and-value", "hour": 16,
                   "why": "GCC trunk coroutine news short alongside the evergreen post"},
    # Fourth episode of the reflect-moc series (signals, slots and thread affinity
    # in the Qt-free core, with the ThreadSanitizer results). It runs beside the
    # evergreen post of the day.
    "2026-10-15": {"slug": "signals-slots-threads-without-qt", "hour": 16,
                   "why": "reflect-moc series episode 4 alongside the evergreen post"},
    # A reactive stdlib short on the std::span initializer_list constructor,
    # beside the evergreen memory-safety post.
    "2026-10-16": {"slug": "span-initializer-list-removed", "hour": 16,
                   "why": "C++26 stdlib news short alongside the evergreen post"},
    # libstdc++ on GCC trunk now rejects a dangling std::pair or std::tuple in
    # every language mode, and two libstdc++ security fixes landed in the same
    # weeks. The short runs beside the evergreen post of the day.
    "2026-10-17": {"slug": "libstdcxx-dangling-pair-tuple", "hour": 16,
                   "why": "libstdc++ trunk and security-fix news alongside the evergreen post"},
    # A library-release short on simdjson 5.0 (reflection officially supported,
    # key selectors, big integers) with a Compiler Explorer demo, beside the
    # evergreen post of the day.
    "2026-10-18": {"slug": "simdjson-5-reflection-supported", "hour": 16,
                   "why": "simdjson 5.0 library news short alongside the evergreen post"},
    # The pre-Buzios mailing closes on 23 October, so the calendar short
    # runs beside the evergreen post (reflection-on-released-gcc) on the
    # 20th while a paper author can still act on the date.
    "2026-10-20": {"slug": "dates-to-watch-buzios-gcc17", "hour": 16,
                   "why": "calendar short ahead of the Buzios meeting and GCC 17 stage 3"},
    # An analysis of the meta-objects Qt Bridges' Rust layer builds at run time,
    # replayed in C++ and diffed against moc. It runs beside the evergreen post
    # (gcc-expansion-named-range) on the 21st.
    "2026-10-21": {"slug": "replay-qt-bridges-meta-objects-against-moc", "hour": 16,
                   "why": "Qt Bridges meta-object analysis alongside the evergreen post"},
    # A toolchain-news short on how Microsoft, the Rust Foundation and Swift 6.4
    # describe working with C++, beside the evergreen post of the day.
    "2026-10-22": {"slug": "rust-swift-cpp-interop-toolchains", "hour": 16,
                   "why": "Rust and Swift interop news alongside the evergreen post"},
    # Reporting under the EU Cyber Resilience Act has applied since 11 September
    # 2026, and Qt shipped a declaration with 6.12 LTS on 30 September, so the
    # fact-only short runs beside the evergreen portable-simd post.
    "2026-10-23": {"slug": "cra-reporting-live-qt-declaration", "hour": 16,
                   "why": "EU CRA reporting news short alongside the evergreen post"},
}


def second_post_hour(date: str, slug: str) -> int:
    """UTC hour to advertise `slug` on `date`. 8 unless it is a planned second."""
    entry = INTENTIONAL_DOUBLES.get(date)
    if entry and entry["slug"] == slug:
        return int(entry["hour"])
    return 8
