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
}


def second_post_hour(date: str, slug: str) -> int:
    """UTC hour to advertise `slug` on `date`. 8 unless it is a planned second."""
    entry = INTENTIONAL_DOUBLES.get(date)
    if entry and entry["slug"] == slug:
        return int(entry["hour"])
    return 8
