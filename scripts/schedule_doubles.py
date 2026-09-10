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
    # CppCon 2026 runs Mon 14 to Fri 18 September in Aurora, CO. The daily
    # conference shorts run ALONGSIDE the scheduled units-series episodes
    # rather than displacing them: the series keeps 08:00Z, and the CppCon
    # post of each day goes out at 16:00Z, after that day's sessions.
    "2026-09-14": {"slug": "cppcon-2026-day-1", "hour": 16,
                   "why": "CppCon day 1 alongside the units series"},
    "2026-09-15": {"slug": "cppcon-2026-day-2", "hour": 16,
                   "why": "CppCon day 2 alongside the units series"},
    "2026-09-16": {"slug": "cppcon-2026-day-3", "hour": 16,
                   "why": "CppCon day 3 alongside the units series"},
    "2026-09-17": {"slug": "cppcon-2026-day-4", "hour": 16,
                   "why": "CppCon day 4 alongside the units series"},
    "2026-09-18": {"slug": "cppcon-2026-day-5", "hour": 16,
                   "why": "CppCon day 5 alongside the units series"},
}


def second_post_hour(date: str, slug: str) -> int:
    """UTC hour to advertise `slug` on `date`. 8 unless it is a planned second."""
    entry = INTENTIONAL_DOUBLES.get(date)
    if entry and entry["slug"] == slug:
        return int(entry["hour"])
    return 8
