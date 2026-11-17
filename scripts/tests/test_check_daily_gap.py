"""Tests for scripts/check_daily_gap.py (stdlib unittest): python3 -m unittest discover -s scripts/tests"""

import importlib.util
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_daily_gap", SCRIPTS / "check_daily_gap.py")
gap = importlib.util.module_from_spec(spec)
sys.modules["check_daily_gap"] = gap
spec.loader.exec_module(gap)

START = date(2026, 11, 18)


def post(directory, day, name, draft=False):
    body = f"---\ntitle: t\npubDate: {day}\n" + ("draft: true\n" if draft else "draft: false\n") + "---\nbody\n"
    (directory / f"{day}-{name}.mdx").write_text(body)


class DailyGapTests(unittest.TestCase):
    def test_a_day_without_a_post_is_a_gap(self):
        self.assertEqual(gap.find_gaps({"2026-11-18", "2026-11-20"}, START, 3), ["2026-11-19"])

    def test_every_day_covered_has_no_gap(self):
        self.assertEqual(gap.find_gaps({"2026-11-18", "2026-11-19"}, START, 2), [])

    def test_two_posts_on_one_day_do_not_cover_the_next_day(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            post(directory, "2026-11-18", "a")
            post(directory, "2026-11-18", "b")
            days = gap.published_days(directory)
        self.assertEqual(gap.find_gaps(days, START, 2), ["2026-11-19"])

    def test_a_draft_does_not_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            post(directory, "2026-11-18", "a", draft=True)
            days = gap.published_days(directory)
        self.assertEqual(gap.find_gaps(days, START, 1), ["2026-11-18"])


if __name__ == "__main__":
    unittest.main()
